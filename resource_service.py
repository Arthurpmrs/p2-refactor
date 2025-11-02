import time
import hashlib
from pathlib import Path
from typing import Dict
from abc import ABC, abstractmethod
from urllib.parse import urlparse


class ResourceService(ABC):
    @abstractmethod
    def upload(self, name: str, data: bytes) -> str:
        pass

    @abstractmethod
    def download(self, url: str) -> bytes:
        pass


class MockResourceService(ResourceService):
    def __init__(self):
        self._store: Dict[str, bytes] = {}

    def upload(self, name: str, data: bytes) -> str:
        key = hashlib.sha256((name + str(time.time())).encode()).hexdigest()
        url = f"https://mock.storage/{key}/{name}"
        self._store[url] = data

        print("⏳ Conectando ao serviço de armazenamento...")
        time.sleep(1)

        print("⬆️ Fazendo upload do recurso...")
        time.sleep(4)

        print("✅ Upload concluído.")

        return url

    def download(self, url: str) -> bytes:
        print("⏳ Conectando ao serviço de armazenamento...")
        time.sleep(1)

        if url not in self._store:
            raise FileNotFoundError(f"resource not found at {url}")

        print("⬇️ Fazendo download do recurso...")
        time.sleep(4)

        print("✅ Download concluído.")

        return self._store[url]


class CachedResourceProxy(ResourceService):
    def __init__(self, upstream: ResourceService):
        self._upstream = upstream
        self._store: Dict[str, bytes] = {}

    def upload(self, name: str, data: bytes) -> str:
        return self._upstream.upload(name, data)

    def is_cached(self, url: str) -> bool:
        return url in self._store

    def download(self, url: str) -> bytes:
        if self.is_cached(url):
            return self._store[url]

        data = self._upstream.download(url)
        self._store[url] = data

        return data

    def clear_cache(self):
        self._store.clear()


class ResourceToFileAdapter:
    download_folder: Path

    def __init__(self, service: ResourceService, download_folder: str = "./resources"):
        self._service = service
        self.set_download_folder(download_folder)

    def set_download_folder(self, folder: str):
        self.download_folder = Path(folder).resolve()
        self.download_folder.mkdir(parents=True, exist_ok=True)

    def _filename_for_url(self, url: str) -> str:
        parsed = urlparse(url)
        name = Path(parsed.path).name

        if name:
            return name

        return hashlib.sha256(url.encode()).hexdigest()

    def upload_from_path(self, str_path: str) -> str:
        path = Path(str_path).resolve()

        if not path.exists():
            raise FileNotFoundError("O arquivo não existe.")

        if path.is_dir():
            raise ValueError("O path representa um diretório.")

        data = path.read_bytes()
        return self._service.upload(path.name, data)

    def download_to_folder(self, url: str) -> Path:
        data = self._service.download(url)

        filename = self._filename_for_url(url)
        path = self.download_folder / filename
        path.write_bytes(data)

        return path
