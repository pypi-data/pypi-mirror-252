import os
import re
from asyncio import Semaphore
from pathlib import Path
from typing import Generator, Tuple, Optional

import httpx
from httpx import HTTPStatusError

WRITE_TIMEOUT = 60 * 3
VALID_NAME_PATTERN = re.compile("^[a-zA-Z0-9_.\-:=\/]+$")
INVALID_NAME_PATTERN = re.compile("[^a-zA-Z0-9_.\-:=\/]+")


def validate_file_path(base: str) -> Optional[str]:
    if not re.match(VALID_NAME_PATTERN, base):
        invalids = "".join(re.findall(INVALID_NAME_PATTERN, base))
        return f"Invalid directory or tag name. Replace the following characters {invalids}, " \
               f"and any spaces if you have them in your directory or tag."
    return None


class Uploader:
    def __init__(self, semaphore: Semaphore, file_path: str, url: str, dev: bool):
        self.semaphore = semaphore
        self.file_path = file_path
        self.url = url
        self.dev = dev

    @staticmethod
    def _get_file(file_path: str) -> dict:
        with open(file_path, 'rb') as fp:
            return {'file': (fp.name, fp)}

    async def upload_file(self, validate: bool = False) -> Tuple[str, bool, Optional[str]]:
        """Asynchronously upload a file to a given URL."""

        if validate and (validation_error := validate_file_path(self.url)):
            return self.file_path, False, validation_error

        try:
            with open(self.file_path, 'rb') as fp:
                files = {'file': (fp.name, fp)}
                async with httpx.AsyncClient(timeout=WRITE_TIMEOUT) as client:
                    async with self.semaphore:
                        async with client.stream('POST', self.url, files=files, params={"dev": self.dev}) as response:
                            try:
                                response.raise_for_status()
                                return self.file_path, True, None
                            except HTTPStatusError as e:  # Ensure we get a 2xx response
                                return self.file_path, False, str(e)
        except httpx.WriteTimeout:
            return self.file_path, False, "Upload took too long, check connection and try again."
        except Exception as e:
            print(e)
            return self.file_path, False, "Something went wrong uploading this file."


def find_files(filepath: Path) -> Generator[str, None, None]:
    pattern = re.compile(r'\.(mp4|mov|jpeg|jpg|png)$')
    for root, dirs, files in os.walk(filepath.absolute()):
        for file in files:
            lowered = file.lower()

            if re.search(pattern, lowered):
                yield os.path.join(root, file)
