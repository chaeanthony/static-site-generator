import re
import os

from pathlib import Path

from markdownblock import markdown_to_html_node


def extract_title(markdown):
    # match = re.search("#{1}\s.*")
    header = markdown.split("\n")[0]
    if header.startswith("# "):
        return header.strip("# ")
    raise Exception("No header found.")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md, template = "", ""
    with open(from_path, "r") as f:
        md = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    file_path = Path(dest_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # for curr_path, dirs, files in os.walk(source_dir):
    #     # Calculate the relative path from the source directory
    #     relative_path = os.path.relpath(curr_path, source_dir)

    #     # Create the corresponding directory in the destination
    #     dest_path = os.path.join(dest_dir, relative_path)
    #     os.makedirs(dest_path, exist_ok=True)

    #     for file in files:
    #         source_file = os.path.join(curr_path, file)
    #         dest_path = os.path.join(dest_path, file.replace(".md", ".html"))
    #         generate_page(source_file, template_path, dest_path)
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
