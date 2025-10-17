import typer
import os
from core.checkers import python_checker, node_checker, dotnet_checker

def check_python(path: str = "./examples/requirements.txt"):
    """Verifica dependencias en un archivo requirements.txt"""
    if (not path.endswith(".txt")):
        typer.echo("❌ El archivo debe tener extensión .txt")
        raise typer.Exit(code=1)
    if (not os.path.isfile(path)):
        typer.echo("❌ El archivo no existe")
        raise typer.Exit(code=1)
    results = python_checker.check_dependencies(path)
    typer.echo("\n🐍 Resultados de dependencias (Python):\n")
    for r in results:
        r.show()

def check_node(path: str = "./examples/package.json"):
    """Verifica dependencias en un archivo package.json de Node.js"""
    if (not path.endswith(".json")):
        typer.echo("❌ El archivo debe tener extensión .json")
        raise typer.Exit(code=1)
    if (not os.path.isfile(path)):
        typer.echo("❌ El archivo no existe")
        raise typer.Exit(code=1)
    package_json = node_checker.load_package_json(path)
    results = node_checker.check_dependencies(package_json)
    typer.echo("\n📦 Resultados de dependencias (Node.js):\n")
    for r in results:
        r.show()

def check_dotnet(path: str = "./examples/Proyecto.csproj"):
    """Verifica dependencias en un archivo .csproj de .NET"""
    if (not path.endswith(".csproj")):
        typer.echo("❌ El archivo debe tener extensión .csproj")
        raise typer.Exit(code=1)
    if (not os.path.isfile(path)):
        typer.echo("❌ El archivo no existe")
        raise typer.Exit(code=1)
    results = dotnet_checker.check_dependencies(path)
    typer.echo("\n🧰 Resultados de dependencias (.NET):\n")
    for r in results:
        r.show()
