import re
import os
import shutil


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def copy_dir(path, to_path):
    if not os.path.exists(to_path):
        os.makedirs(to_path)

    for node in os.listdir(path):
        node_path = os.path.join(path, node)
        dest_path = os.path.join(to_path, node)

        print(f"Copying {node_path} -> {dest_path}")
        if os.path.isfile(node_path):
            shutil.copy(node_path, to_path)
        elif os.path.isdir(node_path):
            copy_dir(node_path, dest_path)
