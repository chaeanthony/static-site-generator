import os

from utils import copy_dir
import shutil

from generatepage import generate_page, generate_pages_recursive

dir_path_public = "./public"
dir_path_static = "./static"
dir_html_template = "./template.html"
dir_markdown = "./content/index.md"
dir_content = "./content"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_dir(dir_path_static, dir_path_public)

    # generate_page(dir_markdown, dir_html_template, "./public/index.html")

    generate_pages_recursive(dir_content, dir_html_template, dir_path_public)


if __name__ == "__main__":
    main()
