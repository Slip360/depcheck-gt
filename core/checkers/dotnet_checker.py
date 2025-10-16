import xml.etree.ElementTree as ET
import requests
from core.models.checker_result import CheckerResult

NUGET_API_URL = "https://api.nuget.org/v3-flatcontainer"

def load_csproj(path: str) -> list[tuple[str, str]]:
    """Carga el archivo .csproj y extrae las dependencias NuGet sin usar namespaces."""
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        packages: list[tuple[str, str]] = []
        for pkg in root.findall(".//PackageReference"):
            name = pkg.attrib.get("Include")
            version = pkg.attrib.get("Version")
            if name and version:
                packages.append((name, version))
        return packages
    except Exception as e:
        print(f"Error al cargar .csproj: {e}")
        return []

def get_latest_version(package_name: str) -> str:
    """Consulta la última versión disponible de un paquete en NuGet."""
    try:
        url = f"{NUGET_API_URL}/{package_name.lower()}/index.json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            versions = data.get("versions", [])
            return versions[-1] if versions else "desconocida"
        else:
            return "error"
    except Exception as e:
        print(f"Error al consultar {package_name}: {e}")
        return "error"

def check_dependencies(csproj_path: str) -> list[CheckerResult]:
    """Verifica las dependencias y devuelve una lista con su estado."""
    results: list[CheckerResult] = []
    packages = load_csproj(csproj_path)
    for name, current_version in packages:
        latest_version = get_latest_version(name)
        status = "actualizado" if current_version == latest_version else "desactualizado"
        results.append(CheckerResult(name, current_version, latest_version, status))
    return results

