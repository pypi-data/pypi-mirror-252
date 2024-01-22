import itertools
import json
import os
import shutil
import sys
import tomllib
from collections import abc
from inspect import signature
from pathlib import Path
from typing import Any

import yaml
from jinja2 import BaseLoader, ChoiceLoader, DictLoader, Environment, FileSystemLoader
from jinja2.environment import load_extensions
from jinja2.utils import import_string
from rich import print

from makejinja.config import Config
from makejinja.plugin import Data, MutableData, PathFilter, Plugin

__all__ = ["makejinja"]


def makejinja(config: Config):
    """makejinja can be used to automatically generate files from [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/templates/)."""

    for path in config.import_paths:
        sys.path.append(str(path.resolve()))

    data = load_data(config)

    if config.output.is_dir() and config.clean:
        if not config.quiet:
            print(f"Remove output '{config.output}'")

        shutil.rmtree(config.output)

    if not single_input_output_file(config):
        config.output.mkdir(exist_ok=True, parents=True)

    env = init_jinja_env(config, data)
    plugins: list[Plugin] = []

    for plugin_name in itertools.chain(config.plugins, config.loaders):
        plugins.append(load_plugin(plugin_name, env, data, config))

    plugin_path_filters: list[PathFilter] = []

    for plugin in plugins:
        if hasattr(plugin, "path_filters"):
            plugin_path_filters.extend(plugin.path_filters())

    # Save rendered files to avoid duplicate work
    # Even if two files are in two separate dirs, they will have the same template name (i.e., relative path)
    # and thus only the first one will be rendered every time
    # Key: output_path, Value: input_path
    rendered_files: dict[Path, Path] = {}

    # Save rendered dirs to later copy metadata
    # Key: output_path, Value: input_path
    rendered_dirs: dict[Path, Path] = {}

    for user_input_path in config.inputs:
        if user_input_path.is_file():
            handle_input_file(user_input_path, config, env, rendered_files)
        elif user_input_path.is_dir():
            handle_input_dir(
                user_input_path,
                config,
                env,
                rendered_files,
                rendered_dirs,
                plugin_path_filters,
            )

    postprocess_rendered_dirs(config, rendered_dirs)


def postprocess_rendered_dirs(
    config: Config,
    rendered_dirs: abc.Mapping[Path, Path],
) -> None:
    # Start with the deepest directory and work our way up, otherwise the statistics could be modified after copying
    for output_path, input_path in sorted(
        rendered_dirs.items(), key=lambda x: x[0], reverse=True
    ):
        if not config.keep_empty and not any(output_path.iterdir()):
            if not config.quiet:
                print(f"Remove empty dir '{output_path}'")

            shutil.rmtree(output_path)

        elif config.copy_metadata:
            if not config.quiet:
                print(f"Copy dir metadata '{input_path}' -> '{output_path}'")

            shutil.copystat(input_path, output_path)


def single_input_output_file(config: Config) -> bool:
    """Check if the user provided a single input and a single output"""
    return (
        len(config.inputs) == 1
        and config.inputs[0].is_file()
        and (config.output.suffix != "" or config.output.is_file())
        and not config.output.is_dir()
    )


def handle_input_file(
    input_path: Path,
    config: Config,
    env: Environment,
    rendered_files: abc.MutableMapping[Path, Path],
) -> None:
    relative_path = Path(input_path.name)
    output_path = generate_output_path(config, relative_path)

    if output_path not in rendered_files:
        render_file(
            input_path,
            str(relative_path),
            output_path,
            config,
            env,
            enforce_jinja_suffix=False,
        )

    rendered_files[output_path] = input_path


def handle_input_dir(
    user_input_path: Path,
    config: Config,
    env: Environment,
    rendered_files: abc.MutableMapping[Path, Path],
    rendered_dirs: abc.MutableMapping[Path, Path],
    plugin_path_filters: abc.Sequence[abc.Callable[[Path], bool]],
) -> None:
    input_paths = (
        input_path
        for include_pattern in config.include_patterns
        for input_path in sorted(user_input_path.glob(include_pattern))
    )

    for input_path in input_paths:
        relative_path = input_path.relative_to(user_input_path)
        output_path = generate_output_path(config, relative_path)

        exclude_pattern_match = any(
            input_path.match(x) for x in config.exclude_patterns
        )
        path_filter_match = any(
            not path_filter(input_path) for path_filter in plugin_path_filters
        )
        if exclude_pattern_match or path_filter_match:
            if not config.quiet:
                print(f"Skip excluded path '{input_path}'")

        elif input_path.is_file() and output_path not in rendered_files:
            render_file(
                input_path,
                str(relative_path),
                output_path,
                config,
                env,
                enforce_jinja_suffix=True,
            )
            rendered_files[output_path] = input_path

        elif input_path.is_dir() and output_path not in rendered_dirs:
            render_dir(input_path, output_path, config)
            rendered_dirs[output_path] = input_path


def generate_output_path(config: Config, relative_path: Path) -> Path:
    if single_input_output_file(config):
        return config.output

    output_file = config.output / relative_path

    if relative_path.suffix == config.jinja_suffix and not config.keep_jinja_suffix:
        output_file = output_file.with_suffix("")

    return output_file


def init_jinja_env(
    config: Config,
    data: Data,
) -> Environment:
    file_loader = DictLoader(
        {path.name: path.read_text() for path in config.inputs if path.is_file()}
    )
    dir_loader = FileSystemLoader([path for path in config.inputs if path.is_dir()])
    loaders: list[BaseLoader] = [file_loader, dir_loader]

    env = Environment(
        loader=ChoiceLoader(loaders),
        extensions=config.extensions,
        block_start_string=config.delimiter.block_start,
        block_end_string=config.delimiter.block_end,
        variable_start_string=config.delimiter.variable_start,
        variable_end_string=config.delimiter.variable_end,
        comment_start_string=config.delimiter.comment_start,
        comment_end_string=config.delimiter.comment_end,
        line_statement_prefix=config.prefix.line_statement,
        line_comment_prefix=config.prefix.line_comment,
        trim_blocks=config.whitespace.trim_blocks,
        lstrip_blocks=config.whitespace.lstrip_blocks,
        newline_sequence=config.whitespace.newline_sequence,  # type: ignore
        keep_trailing_newline=config.whitespace.keep_trailing_newline,
        optimized=config.internal.optimized,
        undefined=config.undefined.value,
        finalize=None,
        autoescape=config.internal.autoescape,
        cache_size=config.internal.cache_size,
        auto_reload=config.internal.auto_reload,
        bytecode_cache=None,
        enable_async=config.internal.enable_async,
    )

    env.globals.update(data)
    env.globals["env"] = os.environ

    return env


def from_yaml(path: Path) -> dict[str, Any]:
    data = {}

    with path.open("rb") as fp:
        for doc in yaml.safe_load_all(fp):
            data |= doc

    return data


def from_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as fp:
        return tomllib.load(fp)


def from_json(path: Path) -> dict[str, Any]:
    with path.open("rb") as fp:
        return json.load(fp)


DATA_LOADERS: dict[str, abc.Callable[[Path], dict[str, Any]]] = {
    ".yaml": from_yaml,
    ".yml": from_yaml,
    ".toml": from_toml,
    ".json": from_json,
}


def collect_files(paths: abc.Iterable[Path], pattern: str = "**/*") -> list[Path]:
    files = []

    for path in paths:
        if path.is_dir():
            files.extend(
                file
                for file in sorted(path.glob(pattern))
                if not file.name.startswith(".") and file.is_file()
            )
        elif path.is_file():
            files.append(path)

    return files


def dict_nested_set(data: MutableData, dotted_key: str, value: Any) -> None:
    """Given `foo`, 'key1.key2.key3', 'something', set foo['key1']['key2']['key3'] = 'something'

    Source: https://stackoverflow.com/a/57561744
    """

    # Start off pointing at the original dictionary that was passed in.
    here = data

    # Turn the string of key names into a list of strings.
    keys = dotted_key.split(".")

    # For every key *before* the last one, we concentrate on navigating through the dictionary.
    for key in keys[:-1]:
        # Try to find here[key]. If it doesn't exist, create it with an empty dictionary. Then,
        # update our `here` pointer to refer to the thing we just found (or created).
        here = here.setdefault(key, {})

    # Finally, set the final key to the given value
    here[keys[-1]] = value


def load_data(config: Config) -> dict[str, Any]:
    data: dict[str, Any] = {}

    for path in collect_files(config.data):
        if loader := DATA_LOADERS.get(path.suffix):
            if not config.quiet:
                print(f"Load data '{path}'")

            data |= loader(path)
        else:
            if not config.quiet:
                print(f"Skip unsupported data '{path}'")

    for key, value in config.data_vars.items():
        dict_nested_set(data, key, value)

    return data


def load_plugin(
    plugin_name: str, env: Environment, data: Data, config: Config
) -> Plugin:
    cls: type[Plugin] = import_string(plugin_name)
    sig_params = signature(cls).parameters
    params: dict[str, Any] = {}

    if sig_params.get("env"):
        params["env"] = env
    if sig_params.get("environment"):
        params["environment"] = env
    if sig_params.get("data"):
        params["data"] = data
    if sig_params.get("config"):
        params["config"] = config

    plugin = cls(**params)

    if hasattr(plugin, "globals"):
        env.globals.update({func.__name__: func for func in plugin.globals()})

    if hasattr(plugin, "functions"):
        env.globals.update({func.__name__: func for func in plugin.functions()})

    if hasattr(plugin, "data"):
        env.globals.update(plugin.data())

    if hasattr(plugin, "extensions"):
        load_extensions(env, plugin.extensions())

    if hasattr(plugin, "filters"):
        env.filters.update({func.__name__: func for func in plugin.filters()})

    if hasattr(plugin, "tests"):
        env.tests.update({func.__name__: func for func in plugin.tests()})

    if hasattr(plugin, "policies"):
        env.policies.update(plugin.policies())

    return plugin


def render_dir(input: Path, output: Path, config: Config) -> None:
    if output.exists() and not config.force:
        if not config.quiet:
            print(f"Skip existing dir '{output}'")
    else:
        if not config.quiet:
            print(f"Create dir '{input}' -> '{output}'")

        output.mkdir(exist_ok=True)


def render_file(
    input: Path,
    template_name: str,
    output: Path,
    config: Config,
    env: Environment,
    enforce_jinja_suffix: bool,
) -> None:
    if output.exists() and not config.force:
        if not config.quiet:
            print(f"Skip existing file '{output}'")

    elif input.suffix == config.jinja_suffix or not enforce_jinja_suffix:
        template = env.get_template(template_name)
        rendered = template.render()

        # Write the rendered template if it has content
        # Prevents empty macro definitions
        if rendered.strip() == "" and not config.keep_empty:
            if not config.quiet:
                print(f"Skip empty file '{input}'")
        else:
            if not config.quiet:
                print(f"Render file '{input}' -> '{output}'")

            with output.open("w") as fp:
                fp.write(rendered)

            if config.copy_metadata:
                shutil.copystat(input, output)

    else:
        if not config.quiet:
            print(f"Copy file '{input}' -> '{output}'")

        shutil.copy2(input, output)
