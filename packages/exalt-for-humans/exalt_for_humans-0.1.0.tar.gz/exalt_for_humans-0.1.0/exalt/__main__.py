""" Elevated Code Images Made Simple
"""

from typing import Optional
from pathlib import Path

import typer

from loguru import logger
from pygments.styles import get_all_styles

from .source import Source

cli = typer.Typer()


@cli.callback(invoke_without_command=True)
def exalt_code(
    ctx: typer.Context,
    output: Path = typer.Option(None, "--output-file", "-o", help="Output file path"),
    begin: int = typer.Option(0, "--begin", "-b", help="Beginning line."),
    count: int = typer.Option(-1, "--count", "-c", help="Number of lines to print."),
    theme: str = typer.Option("monokai", "--theme", "-t", help="Screenshot theme."),
    title: str = typer.Option(None, "--title", "-T", help="Screenshot title."),
    line_numbers: bool = typer.Option(
        False, "--line-numbers", "-L", is_flag=True, help="Number screenshot lines."
    ),
    debug: bool = typer.Option(False, "--debug", "-D", help="Enable debug logging."),
    output_suffix: str = typer.Option(
        ".png", "--output-format", "-f", help="Output format suffix."
    ),
    path: Path = typer.Argument(None, help="Input file path."),
) -> None:
    """Elevated Code Images Made Simple!

    Supply exalt with the path to just about any format file
    and it will generate a beautiful syntax-highlighted
    rendition in a variety of graphical formats (PNG by default).
    """

    (logger.enable if debug else logger.disable)("exalt")

    logger.debug(f"{ctx.invoked_subcommand=}")

    if not ctx.invoked_subcommand:

        if not path:
            print(ctx.get_help())
            raise typer.Exit(code=1)

        if not output_suffix.startswith("."):
            output_suffix = "." + output_suffix

        if not output:
            output = Path.cwd() / path.with_suffix(output_suffix).name
        else:
            output = output.with_suffix(output_suffix)

        logger.debug(f"{path=}")
        logger.debug(f"{output=}")
        logger.debug(f"{begin=} : {count:}")
        logger.debug(f"{theme=}")

        source = Source(
            path,
            begin=begin,
            count=count,
            title=title,
            line_numbers=line_numbers,
            theme=theme,
        )

        try:
            source.save(output)
        except Exception as error:
            typer.secho(f"Uh oh! {error=}", fg="red")
            raise typer.Exit(code=1) from None

        raise typer.Exit(code=0)


@cli.command(name="themes")
def list_themes(ctx: typer.Context) -> None:
    """List available themes."""

    default = "monokai"
    styles = list(get_all_styles())
    width = max(len(style) for style in styles)
    logger.debug(f"{width=}")

    for style in styles:
        if style == default:
            print(f"{style:>20} [default]")
        else:
            print(f"{style:>20}")


if __name__ == "__main__":
    cli()
