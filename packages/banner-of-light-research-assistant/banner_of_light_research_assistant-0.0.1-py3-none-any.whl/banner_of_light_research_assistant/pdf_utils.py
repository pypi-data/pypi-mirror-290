from typing import List
from PyPDF2 import PdfReader, PdfWriter
import os

def reduce_pdf_to_pages(old_pdf: PdfReader, pages: List[int]) -> PdfWriter:
    """
    Reduce the PDF to the specified page numbers.
    """

    new_pdf = PdfWriter()

    for page in pages:
        new_pdf.add_page(old_pdf.pages[page - 1])

    return new_pdf


def cmd_save_message_department_section(pdf_file_path: str) -> None:
    """
    Save the message department section of the Banner of Light PDF.  Always page 6.
    """
    for pdf_file in os.listdir(pdf_file_path):
        pdf = PdfReader(os.path.join(pdf_file_path, pdf_file))
        new_pdf = reduce_pdf_to_pages(pdf, [6])
        new_pdf.write(pdf_file.replace(".pdf", "_page6.pdf"))
