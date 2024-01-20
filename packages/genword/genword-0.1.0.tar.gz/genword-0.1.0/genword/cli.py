from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typer import Argument, Exit, Option, Typer
from typing_extensions import Annotated

from ._utils import generate_combinations

app = Typer()
console = Console()
__version__ = '0.1.0'


def version_callback(value: bool):
    """Show the version of the application and exit."""
    if value:
        console.print('[bold]Genword[/bold] version: ', end='')
        print(__version__)
        console.print('https://github.com/henriquesebastiao/genword')
        raise Exit()


@app.command()
def main(
    characters: Annotated[
        str,
        Argument(
            help='Character string from which the combinations will be generated',
        ),
    ] = r'abcdefghijklmnopqrstuvwxyz1234567890!@#$%&',  # noqa
    min_length: Annotated[
        int, Argument(help='Minimum amount of characters in each combination')
    ] = 1,
    max_length: Annotated[
        int, Argument(help='Maximum number of characters in each combination')
    ] = 8,
    file_name: Annotated[
        str,
        Option(
            '--file-name',
            '-f',
            help='Name of the .txt output file containing the generated words',
        ),
    ] = 'words',
    verbose: Annotated[
        bool,
        Option(
            '--verbose',
            '-v',
            help='Prints each word generated on the terminal',
        ),
    ] = False,
    version: Annotated[  # noqa: F841
        Optional[bool],
        Option(
            '--version',
            callback=version_callback,
            help='Returns the version of Wordlist-Gen',
        ),
    ] = None,
):
    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        transient=True,
    ) as progress:
        progress.add_task(
            description='Generating...', total=None
        )  # Adiciona animação radial de progresso

        with open(f'{file_name}.txt', 'w') as file:
            total_words = 0
            for x in generate_combinations(characters, min_length, max_length):
                file.write(f'{x}\n')
                if verbose:
                    console.print(x)
                total_words += 1

    console.print(
        '[bold green]Done![/bold green] [yellow]:high_voltage:[/yellow]'
    )
    console.print(f'{total_words} words generated')
    console.print(f'File saved as: [bold]{file_name}.txt[/bold]')
