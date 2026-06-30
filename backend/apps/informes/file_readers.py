from abc import ABC, abstractmethod
import io

from docx import Document
from pypdf import PdfReader


class BaseFileReader(ABC):
    """Template Method para lectura de archivos académicos."""

    def read(self, archivo) -> str:
        content = self._read_bytes(archivo)
        parsed = self._parse_content(content)
        return self._normalize_text(parsed)

    def _read_bytes(self, archivo) -> bytes:
        return archivo.read()

    @abstractmethod
    def _parse_content(self, content: bytes) -> str:
        raise NotImplementedError

    def _normalize_text(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return '\n'.join(lines)


class DocxFileReader(BaseFileReader):
    def _parse_content(self, content: bytes) -> str:
        doc = Document(io.BytesIO(content))
        return '\n'.join(para.text.strip() for para in doc.paragraphs if para.text.strip())


class PdfFileReader(BaseFileReader):
    def _parse_content(self, content: bytes) -> str:
        reader = PdfReader(io.BytesIO(content))
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text() or ''
            if page_text.strip():
                text_parts.append(page_text.strip())
        return '\n'.join(text_parts)


def build_file_reader(file_name: str) -> BaseFileReader:
    lower_name = file_name.lower()
    if lower_name.endswith('.docx'):
        return DocxFileReader()
    if lower_name.endswith('.pdf'):
        return PdfFileReader()
    raise ValueError('Formato de archivo no soportado.')
