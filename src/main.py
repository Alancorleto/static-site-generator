from src.file_manager import copy_folder_contents
from src.page_generator import generate_pages_recursive


def main():
    copy_folder_contents("static", "public")
    generate_pages_recursive("content/", "template.html", "public/")


if __name__ == "__main__":
    main()
