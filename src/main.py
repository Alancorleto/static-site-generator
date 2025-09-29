from src.file_manager import copy_folder_contents
from src.page_generator import generate_page


def main():
    copy_folder_contents("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
