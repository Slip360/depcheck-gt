import typer

class CheckerResult:
    """Clase para representar el resultado de la verificación de una dependencia."""

    def __init__(self, package: str, current_version: str, latest_version: str, status: str) -> None:
        """Inicializa una instancia de CheckerResult."""
        self._package = package
        self._current_version = current_version
        self._latest_version = latest_version
        self._status = status
    
    def show(self) -> None:
        """Muestra el resultado de la verificación en la consola."""
        typer.echo(f"- {self._package}: {self._current_version} → {self._latest_version} [{self._status}]")
