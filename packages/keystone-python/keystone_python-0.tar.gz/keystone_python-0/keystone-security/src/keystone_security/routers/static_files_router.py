from pathlib import Path
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import FileResponse

from keystone_security.settings import static_files_settings

router = APIRouter()


@router.get("/unauthorized")
def unauthorized():
    return {
            "message": "Unauthorized"
    }


@router.get("/{rest_of_path:path}", response_class=FileResponse)
def get_file(
        rest_of_path: Optional[str] = None,
):
    settings = static_files_settings.get_settings()
    file_path = rest_of_path if rest_of_path else "index.html"
    root_path = Path(settings.dir)

    if not (root_path / file_path).exists() or (root_path / file_path).is_dir():
        file_path = "index.html"
    return root_path / file_path
