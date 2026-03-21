"""Leitor de PDF - Extrai texto de arquivos PDF."""

import io
import logging

logger = logging.getLogger(__name__)


class PDFReader:
    """Leitor de PDF que extrai texto."""

    def __init__(self):
        self._has_pypdf2 = self._check_pypdf2()
        self._has_pdfplumber = self._check_pdfplumber()

    def _check_pypdf2(self) -> bool:
        try:
            import PyPDF2  # noqa: F401
            return True
        except ImportError:
            return False

    def _check_pdfplumber(self) -> bool:
        try:
            import pdfplumber  # noqa: F401
            return True
        except ImportError:
            return False

    def extract_text(self, pdf_content: bytes) -> str:
        if self._has_pdfplumber:
            return self._extract_with_pdfplumber(pdf_content)
        if self._has_pypdf2:
            return self._extract_with_pypdf2(pdf_content)
        raise ImportError("Instale PyPDF2 ou pdfplumber para processar PDFs")

    def _extract_with_pdfplumber(self, pdf_content: bytes) -> str:
        import pdfplumber

        text = []
        with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return "\n".join(text).strip()

    def _extract_with_pypdf2(self, pdf_content: bytes) -> str:
        import PyPDF2

        text = []
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return "\n".join(text).strip()
