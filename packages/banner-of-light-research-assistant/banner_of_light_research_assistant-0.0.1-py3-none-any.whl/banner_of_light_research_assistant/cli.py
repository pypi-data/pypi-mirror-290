from banner_of_light_research_assistant.pdf_utils import cmd_save_message_department_section
import argparse

def main():
    parser = argparse.ArgumentParser(description="Save the message department section of the Banner of Light PDF")

    subparsers = parser.add_subparsers(dest="reduce_to_message_department_section") 
    reduce_to_message_department_parser = subparsers.add_parser("save_message_department_section")
    reduce_to_message_department_parser.add_argument("--pdf-files-path", required=True, help="Path to the Banner of Light PDF file")

    args = parser.parse_args()

    cmd_save_message_department_section(args.pdf_files_path)