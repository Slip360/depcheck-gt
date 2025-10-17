import typer
import os
from typing import Union, Literal
from core.functions import checker_functions

app: typer.Typer = typer.Typer(help="🔍 DepCheck GT: Verificador de dependencias obsoletas")

@app.command()
def check(language: Literal['python', 'node', 'c#'] = 'python', path: str = './examples/requirements.txt') -> None:
    """Verifica dependencias en el archivo especificado."""
    if language == 'python' and path.endswith('.txt'):
        checker_functions.check_python(path)
    elif language == 'node' and path.endswith('.json'):
        checker_functions.check_node(path)
    elif language == 'c#' and path.endswith('.csproj'):
        checker_functions.check_dotnet(path)
    else:
        typer.echo("Lenguaje no soportado o extensión de archivo no válida.")

if __name__ == "__main__":
    app()
