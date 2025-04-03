import os

import requests
from _back.src.shared.config.settings import FILE_DIR, MODELS_DIR
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

from externals.context import Context
from models.entities.echo_entity import EchoEntity
from repositories.echo_repository import index_echo_content_to_qdrant
from utils import slack_utils as slack_utils

context = Context()


class EchoService:
    ECHO: EchoEntity = None

    def __init__(self, echo: EchoEntity = None):
        self.ECHO = echo

    def _download_file(self) -> str:
        if self.ECHO and hasattr(self.ECHO, "file_url") and self.ECHO.file_url:
            extention = os.path.basename(self.ECHO.file_url).split(".")[-1].split("?")[0]
            file_path = FILE_DIR / f"ECHO-{self.ECHO.cod}.{extention}"

            response = requests.get(self.ECHO.file_url)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                return file_path
            else:
                raise Exception(f"Failed to download file: {response.status_code}")
        else:
            raise ValueError("No URL found in the Echo entity")

    def _remove_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)

    def index_echo(self):
        try:
            file_path = self._download_file()

            pipeline_options = PdfPipelineOptions(artifacts_path=MODELS_DIR / "docling" / "models")
            converter = DocumentConverter(
                format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
            )

            doc_echo = converter.convert(file_path)
            content_markdown = doc_echo.document.export_to_markdown()
            content_markdown = content_markdown.replace("<!-- image -->", "")

            self._remove_file(file_path)

            index_echo_content_to_qdrant(content_markdown)

            return True

        except Exception as err:
            raise err
