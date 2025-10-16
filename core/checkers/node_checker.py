import json
import requests
from typing import Any
from core.models.checker_result import CheckerResult

NPM_REGISTRY_URL = "https://registry.npmjs.org"

def load_package_json(path: str) -> dict[Any, Any]:
    """Carga el archivo package.json desde la ruta especificada."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar package.json: {e}")
        return {}

def get_latest_version(package_name: str) -> str:
    """Consulta la última versión disponible de un paquete en npm."""
    try:
        response = requests.get(f"{NPM_REGISTRY_URL}/{package_name}")
        if response.status_code == 200:
            data = response.json()
            return data.get("dist-tags", {}).get("latest", "desconocida")
        else:
            return "error"
    except Exception as e:
        print(f"Error al consultar {package_name}: {e}")
        return "error"

def check_dependencies(package_json: dict[Any, Any]) -> list[CheckerResult]:
    """Verifica las dependencias y devuelve una lista con su estado."""
    results: list[CheckerResult] = []
    dependencies = package_json.get("dependencies", {})
    for name, current_version in dependencies.items():
        latest_version = get_latest_version(name)
        status = "actualizado" if current_version.replace("^", "").replace("~", "") == latest_version else "desactualizado"
        results.append(CheckerResult(name, current_version, latest_version, status))
    return results
