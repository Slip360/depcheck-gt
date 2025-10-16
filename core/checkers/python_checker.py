import requests
from pathlib import Path
from core.models.checker_result import CheckerResult

PYPI_API_URL = "https://pypi.org/pypi"

def load_requirements(path: str) -> list[tuple[str | None, str | None]]:
    """Carga el archivo requirements.txt y extrae paquetes con sus versiones."""
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
        packages: list[tuple[str | None, str | None]] = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "==" in line:
                name, version = line.split("==")
                packages.append((name.strip(), version.strip()))
            else:
                packages.append((line.strip(), None))
        return packages
    except Exception as e:
        print(f"Error al cargar requirements.txt: {e}")
        return []

def get_latest_version(package_name: str) -> str:
    """Consulta la última versión disponible de un paquete en PyPI."""
    try:
        response = requests.get(f"{PYPI_API_URL}/{package_name}/json")
        if response.status_code == 200:
            data = response.json()
            return data.get("info", {}).get("version", "desconocida")
        else:
            return "error"
    except Exception as e:
        print(f"Error al consultar {package_name}: {e}")
        return "error"

def check_dependencies(requirements_path: str) -> list[CheckerResult]:
    """Verifica las dependencias y devuelve una lista con su estado."""
    results: list[CheckerResult] = []
    packages = load_requirements(requirements_path)
    for name, current_version in packages:
        if (not name):
            continue
        latest_version = get_latest_version(name)
        if current_version:
            status = "actualizado" if current_version == latest_version else "desactualizado"
        else:
            status = "sin versión especificada"
        results.append(CheckerResult(name, current_version or "no especificada", latest_version, status))
    return results
