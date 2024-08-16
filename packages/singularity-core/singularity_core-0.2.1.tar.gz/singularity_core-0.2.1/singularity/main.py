import importlib.util
import inspect
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI


class Singularity(FastAPI):
    def __init__(self, env_path: str = None):
        self.base_path: str = Path(inspect.stack()[1].filename).parent
        self.services_folder: str = self.base_path / "services"
        self.services_path: list = []
        self.setup_application()
        self._load_env_(env_path)

    def _load_env_(self, path: str | None):
        if path is None:
            path = os.path.join(self.base_path, ".env")

        if not os.path.exists(path):
            raise ValueError(f"Environment file not found in {path}")

        load_dotenv(dotenv_path=path)

    def setup_application(
        self,
    ):
        self.app = FastAPI()
        router = self.register_services()
        self.app.include_router(router)

    def __getattr__(self, name):
        # This method is called when an attribute is not found in the usual places.
        # It delegates attribute access to the FastAPI instance.
        return getattr(self.app, name)

    @staticmethod
    def service_name_validation(name: str) -> None | ValueError:
        if any(c in name for c in " /\\.:?\"<>*[]=;,!@#$%^&()+`~'"):
            print(
                f"Service name: {name} should contain only alphabets, numbers, and underscores."
            )
            return False
        else:
            return True

    def register_services(self):
        router: APIRouter = APIRouter()
        services_path: list = []
        for root, dirs, files in os.walk(self.services_folder):
            if "service.py" in files:
                route = root.replace(str(self.services_folder), "")
                services_path.append((route, root))

        for route_prefix, service_path in services_path:
            spec = importlib.util.spec_from_file_location(
                "service", str(service_path) + "/service.py"
            )
            module = importlib.util.module_from_spec(spec)
            module.__package__ = f"services{route_prefix.replace('/', '.')}"
            spec.loader.exec_module(module)

            if hasattr(module, "Service"):
                print(f"Registering service at {route_prefix}")
                service_class = getattr(module, "Service")
                service_instance = service_class()
                for http_method in ["get", "post", "put", "delete"]:
                    if hasattr(service_instance, http_method):
                        router.add_api_route(
                            route_prefix.replace("|", "/"),
                            getattr(service_instance, http_method),
                            methods=[http_method.upper()],
                        )
            else:
                raise ValueError(f"Service class not found in {str(service_path)}")

        return router
