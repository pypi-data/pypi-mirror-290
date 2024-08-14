from unittest import TestCase

from PyPDF2 import PdfReader
from banner_of_light_research_assistant.pdf_utils import (
    reduce_pdf_to_pages,
)


class TestPdfUtils(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.test_pdf_file = "tests/test_data/banner_of_light_v96_n6_1_oct_1904.pdf"

    def test_reduce_pdf_to_pages(self):

        old_pdf = PdfReader(self.test_pdf_file)
        new_pdf = reduce_pdf_to_pages(old_pdf, [6, 7])
        self.assertEqual(len(new_pdf.pages), 2)
