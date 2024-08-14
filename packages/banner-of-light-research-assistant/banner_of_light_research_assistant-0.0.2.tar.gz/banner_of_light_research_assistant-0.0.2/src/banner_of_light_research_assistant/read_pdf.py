#!/usr/bin/python3
"""
This script is used to prepare the documents for researching 
by extracting the text from the pdf files and saving them in
a text file.

Data Quality Issues:

1. Multiple columns of text run together.
2. Words may be split across lines.
3. Words may be missing from the text.
"""

from typing import List
import pdfplumber
import numpy
from pdfplumber.pdf import Page
import cv2

def transform_contour_to_order(contour: cv2.typing.Rect) -> tuple[int, int, int, int]:
    """
    contours points are not in a specific order.  This will convert them to left, top, right, bottom ordering.
    """
    x, y, w, h = contour
    return (x, y, x + w, y + h)


def filter_bounding_boxes_to_columns(bounding_boxes: List[cv2.typing.Rect]) -> List[cv2.typing.Rect]:
    """
    filter out all bounding boxes that are not columns.

    1. left minus right must be greater than pagewidth
    """
    pass


def detect_columns_from_pdf(pdf_page: Page) -> List[tuple]:

    image = numpy.array(pdf_page.to_image().original)  # Convert image to NumPy array

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("gray_image.png", image_gray)
    _, thresh = cv2.threshold(image_gray, 120, 255, cv2.THRESH_BINARY_INV)

    # Dilate the image to connect text areas
   # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 15))
   # dilated = cv2.dilate(thresh, kernel, iterations=2)

    # First, dilate with a larger vertical kernel to connect text blocks within columns
    kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
    dilated = cv2.dilate(thresh, kernel_dilate, iterations=2)

    # Next, erode slightly to break connections between columns
    kernel_erode = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 10))
    eroded = cv2.erode(dilated, kernel_erode, iterations=2)

    # Combine the effects by applying a final dilation
    kernel_dilate_final = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))
    dilate_final = cv2.dilate(eroded, kernel_dilate_final, iterations=4)

    kernel_erode_final = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
    processed = cv2.dilate(dilate_final, kernel_erode_final, iterations=2)

    # Save the dilated image
    cv2.imwrite("dilated_image.png", dilated)
    cv2.imwrite("eroded_image.png", eroded)
    cv2.imwrite("final_dilate.png", dilate_final)
    cv2.imwrite("processed.png", processed)

    # Find contours
    contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print("Found", len(contours), "contours")

    # Filter out small contours and find bounding boxes
    bounding_boxes = [
        transform_contour_to_order(cv2.boundingRect(contour))
        for contour in contours
        if cv2.contourArea(contour) > 100
    ]


    # Sort bounding boxes by x coordinate
    bounding_boxes.sort(key=lambda x: x[0])

    return bounding_boxes

def get_text_from_pdf_page(pdf_page: Page, column_boundaries: List[tuple]) -> str:
    """
    Extract the text from the specified columns of the pdf page.

    Parameters:
    pdf_page (Page): The pdf page to extract text from.
    column_boundaries (List[tuple]): The list of column boundaries to extract.

    Returns:
    str: The text extracted from the pdf page.
    """
    text = ""
    for left, top, right, bottom in column_boundaries:
        page_column = pdf_page.within_bbox((left, top, right, bottom))
        text += page_column.extract_text()

    return text

def get_text_from_pdf(pdf_file: str, page_numbers: None | List[int] = None) -> str:
    """
    Extract the text from the specified pages of the pdf file.

    Parameters:
    page_numbers (List[int]): The list of page numbers to extract.
    pdf_file (str): The path to the pdf file.

    Returns:
    str: The text extracted from the pdf file.
    """

    column_count = 5

    with pdfplumber.open(pdf_file, page_numbers) as pdf:
        text = ""
        for page in pdf.pages:
            column_width = page.width / column_count

            for column in range(column_count):
                left_boundary = column * column_width
                top_boundary = float(0)
                right_boundary = (column + 1) * column_width
                bottom_boundary = page.height - 0.1

                page_column = page.within_bbox(
                    (left_boundary, top_boundary, right_boundary, bottom_boundary)
                )

                text += page_column.extract_text()

        return text
