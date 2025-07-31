from fastapi import APIRouter
import importlib
import pkgutil
import os

router = APIRouter()

package_name = __name__  # "app.routes.api"

for _, module_name, is_pkg in pkgutil.iter_modules([os.path.dirname(__file__)]):
    if not is_pkg and module_name != "__init__":
        module = importlib.import_module(f"{package_name}.{module_name}")
        if hasattr(module, "router"):
            router.include_router(module.router, prefix=f"/{module_name}")
