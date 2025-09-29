import sys
from src.file_manager import copy_folder_contents
from src.page_generator import generate_pages_recursive



def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    copy_folder_contents("static", "docs")
    generate_pages_recursive("content/", "template.html", "docs/", base_path)


if __name__ == "__main__":
    main()
