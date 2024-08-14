from unittest import TestCase

import pdfplumber
from banner_of_light_research_assistant.read_pdf import (
    get_text_from_pdf,
    get_text_from_pdf_page,
    detect_columns_from_pdf,
)


class TestPrepareData(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.test_pdf_file = "tests/test_data/banner_of_light_v96_n6_1_oct_1904.pdf"

        self.pdf = pdfplumber.open(self.test_pdf_file)

    def test_get_text_from_pdf(self):
        pdf_file = "tests/test_data/banner_of_light_v96_n6_1_oct_1904.pdf"
        page_numbers = [6]
        result = get_text_from_pdf(pdf_file, page_numbers)
        print(result)

        self.assertTrue(result.startswith("EDITED BY\nMINNIE RESERVE SOCLE."), result[:100])


    def test_get_text_from_pdf_page(self):
        test_page = self.pdf.pages[5]

        column_boundaries = [
            (29, 65, 193, 1270),
            (193, 65, 354, 1270),
            (354, 65, 519, 1270),
            (519, 65, 678, 1270),
            (678, 65, 853, 1270),
        ]

        result = get_text_from_pdf_page(test_page, column_boundaries)

        self.assertTrue(result.startswith("®nr |§omc airdt"), result)

    def test_detect_columns_from_pdf(self):

        test_page = self.pdf.pages[5]

        result = detect_columns_from_pdf(test_page)
        print(result)

        def draw_detected_columns_on_image():
            try:
                test_evalulation_results = test_page.to_image().draw_rects(
                    result, stroke_width=2
                )

                test_evaluation_results_filename = self.test_pdf_file.replace(
                    ".pdf", f"_column_results_{test_page.page_number}.png"
                )
                test_evalulation_results.save(
                    test_evaluation_results_filename, format="PNG"
                )
            except ValueError as e:
                print("Could not generate column image.", e)

        expected_result = [
            (29, 65, 193, 1270),
            (193, 65, 354, 1270),
            (354, 65, 519, 1270),
            (519, 65, 678, 1270),
            (678, 65, 853, 1270),
        ]

        try:
            self.assertEqual(len(result), len(expected_result), result)
        except AssertionError as e:
            draw_detected_columns_on_image()
            raise e

        # Assert that result matches the expected result within a margin of error of 5%
        for i, (left, top, right, bottom) in enumerate(result):
            message = f"Expected: {expected_result[i]}, Got: {result[i]}"
            try:
                self.assertLessEqual(abs(left - expected_result[i][0]), 5, message)
                self.assertLessEqual(abs(top - expected_result[i][1]), 5, message)
                self.assertLessEqual(abs(right - expected_result[i][2]), 5, message)
                self.assertLessEqual(abs(bottom - expected_result[i][3]), 5, message)
            except AssertionError as e:
                draw_detected_columns_on_image()
                raise e
