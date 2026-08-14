import os
import shutil
from pathlib import Path
from typing import BinaryIO
import uuid

class StorageProvider:
    """Abstract interface for object storage."""
    
    async def upload(self, file_obj: BinaryIO, path: str) -> str:
        raise NotImplementedError
        
    async def delete(self, path: str) -> bool:
        raise NotImplementedError
        
    async def download(self, path: str) -> BinaryIO:
        raise NotImplementedError
        
    async def move(self, source_path: str, destination_path: str) -> str:
        raise NotImplementedError
        
    def create_directory(self, path: str) -> str:
        raise NotImplementedError

class LocalStorageProvider(StorageProvider):
    """Local file system implementation of the StorageProvider interface."""
    
    def __init__(self, base_path: str = "storage"):
        # Use absolute path relative to the backend project root
        project_root = Path(__file__).parent.parent.parent
        self.base_path = (project_root / base_path).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)
        
    def _get_absolute_path(self, relative_path: str) -> Path:
        """Resolves relative paths and prevents directory traversal attacks."""
        safe_path = (self.base_path / relative_path).resolve()
        if self.base_path not in safe_path.parents and safe_path != self.base_path:
            raise ValueError(f"Path traversal detected or invalid storage path: {relative_path}")
        return safe_path

    async def upload(self, file_obj: BinaryIO, path: str) -> str:
        """Uploads a file-like object to the specified relative path."""
        target_path = self._get_absolute_path(path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(target_path, "wb") as buffer:
            shutil.copyfileobj(file_obj, buffer)
            
        return path

    async def delete(self, path: str) -> bool:
        """Deletes a file or directory at the specified relative path."""
        target_path = self._get_absolute_path(path)
        if target_path.exists():
            if target_path.is_dir():
                shutil.rmtree(target_path)
            else:
                target_path.unlink()
            return True
        return False

    async def download(self, path: str) -> BinaryIO:
        """Returns a file object for reading."""
        target_path = self._get_absolute_path(path)
        if not target_path.exists() or not target_path.is_file():
            raise FileNotFoundError(f"File not found in storage: {path}")
        return open(target_path, "rb")

    async def move(self, source_path: str, destination_path: str) -> str:
        """Moves/renames a file or directory."""
        src = self._get_absolute_path(source_path)
        dst = self._get_absolute_path(destination_path)
        
        if not src.exists():
            raise FileNotFoundError(f"Source not found in storage: {source_path}")
            
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        return destination_path

    def create_directory(self, path: str) -> str:
        """Creates a directory at the specified relative path."""
        target_path = self._get_absolute_path(path)
        target_path.mkdir(parents=True, exist_ok=True)
        return path

# Global storage service instance. 
# In the future, this can be swapped out based on settings (e.g. S3StorageProvider)
storage_service = LocalStorageProvider(base_path="storage")
