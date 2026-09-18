# -----------------------------------------------------------------------
# CLI Entrypoint
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import logging
import sys
from typing import Any, NoReturn

# Third-party modules
import click
from gufo.loader import Loader

# Gufo Tower modules
from gufo.tower.models.environment import Environment


class Context:
    """CLI execution context."""

    def __init__(self) -> None:
        self._verbose = False

    @property
    def verbose(self) -> bool:
        """Whether verbose output is enabled."""
        return self._verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        """Enable or disable verbose output.

        Args:
            value: Whether to enable verbose logging.
        """
        self._verbose = value
        logging.basicConfig(
            level=logging.DEBUG if value else logging.INFO,
            format="%(asctime)s [%(name)s] %(message)s",
        )

    def print(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Print a message to standard output.

        Args:
            *args: Positional arguments passed to `print`
            **kwargs: Keyword arguments passed to `print`.
        """
        print(*args, **kwargs)

    def debug(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Print a debug message to standard output if verbose mode is enabled.

        Args:
            *args: Positional arguments passed to `print`
            **kwargs: Keyword arguments passed to `print`.
        """
        if self._verbose:
            print(*args, **kwargs)

    def die(self, msg: str) -> NoReturn:
        """Print an error message and terminate the process.

        Args:
            msg: Error message to print.
        """
        self.print(msg)
        sys.exit(1)

    def get_environment(self, name: str | None) -> Environment:
        """Get an environment by name or resolve the default environment.

        If a name is specified, the environment with the given name is returned.
        If no name is specified and only one environment exists, that environment
        is returned. Otherwise, the default environment is used.

        Args:
            name: Optional environment name. If omitted, resolve the environment
                automatically.

        Returns:
            Resolved environment.

        Raises:
            SystemExit: If the specified environment does not exist or multiple
                environments exist without a default environment.
        """
        # Explicit name
        if name:
            try:
                return Environment.get(Environment.name == name)
            except Environment.DoesNotExist:
                self.die(f"Invalid environment: '{name}'")
        # Single environment
        environments = list(Environment.select().limit(2))
        if len(environments) == 1:
            return environments[0]
        # Default environment
        try:
            return Environment.get(Environment.is_default)
        except Environment.DoesNotExist:
            self.die(
                "Multiple environments exist, select one with `--env` option"
            )


pass_context = click.make_pass_decorator(Context, ensure=True)


class Entrypoint:
    """CLI entrypoint registered with the Gufo Loader.

    Args:
        fn: Click command associated with the entrypoint.
    """

    def __init__(self, fn: click.Command) -> None:
        self.fn = fn
        self.__module__ = fn.callback.__module__


def entrypoint(fn: click.Command) -> Entrypoint:
    """Register a Click command as a Gufo Tower CLI entrypoint.

    The decorator must be applied to a command created by
    `click.command`.

    Example::

        @entrypoint
        @click.command("version", short_help="Show Gufo Tower version")
        def version() -> None:
            ...

    Args:
        fn: Click command to register.

    Returns:
        Entrypoint wrapping the Click command.
    """
    return Entrypoint(fn)


loader = Loader[Entrypoint](base="gufo.tower.cli", exclude="base")


class CLIDispatcher(click.Group):
    """Click command group that dynamically discovers CLI entrypoints."""

    def list_commands(self, ctx: Context) -> list[str]:
        """List available CLI commands.

        Args:
            ctx: Current CLI context.

        Returns:
            Sorted list of available command names.
        """
        return sorted(loader)

    def get_command(self, ctx: Context, name: str) -> click.Command | None:
        """Get a CLI command by name.

        Args:
            ctx: Current CLI context.
            name: Command name.

        Returns:
            The corresponding Click command, or ``None`` if the command is not found.
        """
        wrapper = loader.get(name.replace("-", "_"))
        if wrapper is None:
            return None
        return wrapper.fn


@click.command(
    cls=CLIDispatcher, context_settings={"auto_envvar_prefix": "TOWER"}
)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@pass_context
def main(ctx: Context, verbose: bool) -> None:
    """Gufo Tower command-line interface.

    Args:
        ctx: Current CLI context.
        verbose: Enable verbose output.
    """
    ctx.verbose = verbose
