from htmlnode import LeafNode
from utils import extract_markdown_images, extract_markdown_links

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text: str, text_type: str, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for old in old_nodes:
        if old.text_type != text_type_text:
            res.append(old)  # only split text_type_text nodes
            continue
        split_nodes = []
        split_text = old.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError(
                "Invalid Markdown Syntax"
            )  # delimiter must have matching closing delimiter

        for i, txt in enumerate(split_text):
            if txt == "":
                continue

            if i % 2 == 0:
                split_nodes.append(TextNode(txt, text_type_text))
            else:
                split_nodes.append(TextNode(txt, text_type))

        res.extend(split_nodes)

    return res


def split_nodes_image(old_nodes: list[TextNode]):
    res = []
    for old in old_nodes:
        if old.text_type != text_type_text:
            res.append(old)
            continue

        old_text = old.text
        extracted = extract_markdown_images(old_text)
        if len(extracted) == 0:  # no extracted images, append original node
            res.append(old)
            continue

        # extract links and create TextNodes
        for alt, href in extracted:
            sections = old_text.split(f"![{alt}]({href})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, element not closed")
            if sections[0]:
                res.append(TextNode(sections[0], text_type_text))
            res.append(TextNode(alt, text_type_image, href))

            old_text = sections[1]
        if old_text:  # add last text not handled in loop
            res.append(TextNode(old_text, text_type_text))
    return res


def split_nodes_link(old_nodes: list[TextNode]):
    res = []
    for old in old_nodes:
        if old.text_type != text_type_text:
            res.append(old)
            continue

        old_text = old.text
        extracted_links = extract_markdown_links(old_text)
        if len(extracted_links) == 0:  # no extracted images, append original node
            res.append(old)
            continue

        # extract links and create TextNodes
        for txt, href in extracted_links:
            sections = old_text.split(f"[{txt}]({href})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, element not closed")

            if sections[0]:
                res.append(TextNode(sections[0], text_type_text))
            res.append(TextNode(txt, text_type_link, href))

            old_text = sections[1]
        if old_text:  # add last text not handled in loop
            res.append(TextNode(old_text, text_type_text))
    return res


def text_to_textnodes(text):
    return split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_link(
                        split_nodes_image([TextNode(text, text_type_text)])
                    ),
                    "**",
                    text_type_bold,
                ),
                "`",
                text_type_code,
            ),
            "*",
            text_type_italic,
        ),
        "_",
        text_type_italic,
    )
