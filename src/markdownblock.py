import re

from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node, text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n") if block]


def block_to_block_type(block: str) -> str:
    lines = block.split("\n")
    if re.match(r"^#{1,6}\s\w+", block):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if line.startswith(">"):
                continue
            return block_type_paragraph
        return block_type_quote
    if re.match(r"^\*\s|^-\s", block, re.MULTILINE):
        return block_type_ulist
    if re.match(r"^\d\.\s", block, re.MULTILINE):
        return block_type_olist

    return block_type_paragraph


def markdown_to_html_node(markdown: str) -> HTMLNode:
    html_node = ParentNode("div", [])

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_heading:
            html_node.children.append(md_header_to_html_node(block))
        elif block_type == block_type_paragraph:
            html_node.children.append(md_paragraph_to_html_node(block))
        elif block_type == block_type_code:
            html_node.children.append(md_code_to_html_node(block))
        elif block_type == block_type_quote:
            html_node.children.append(md_quote_to_html_node(block))
        elif block_type == block_type_olist:
            html_node.children.append(md_ol_to_html_node(block))
        elif block_type == block_type_ulist:
            html_node.children.append(md_ul_to_html_node(block))

    return html_node


def text_to_leaf_nodes(text: str) -> list[HTMLNode]:
    """
    Parses markdown text to LeafNodes
    """
    text_nodes = text_to_textnodes(text)
    res = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)  # convert TextNode to LeafNodes
        res.append(html_node)
    return res


def md_header_to_html_node(md_header: str) -> HTMLNode:
    """helper method to convert markdown header to html node"""
    header_size = 0
    for char in md_header:
        if char != "#":
            break
        header_size += 1

    if header_size > 6 or header_size + 1 >= len(
        md_header
    ):  # expect 1 space to follow header. ex: ## text
        return ValueError("invalid header")

    return ParentNode(
        f"h{header_size}", text_to_leaf_nodes(md_header[header_size + 1 :])
    )


def md_paragraph_to_html_node(md_paragraph: str) -> list[HTMLNode]:
    """
    helper method to convert markdown paragraph to html parent node containing children nodes, if any

    Example:
    md_paragraph:
    This is another paragraph with *italic* text and `code` here
    This is the same paragraph on a new line

    output:
    ParentNode(p, [LeafNode()...])
    """
    lines = md_paragraph.split("\n")
    paragraph = " ".join(lines)
    children = text_to_leaf_nodes(paragraph)
    return ParentNode("p", children)


def md_code_to_html_node(md_code: str) -> HTMLNode:
    if not md_code.startswith("```") or not md_code.endswith("```"):
        raise ValueError("Invalid code block")
    text = md_code[4:-3]
    children = text_to_leaf_nodes(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def md_quote_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    quote_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid Quote Markdown")
        quote_lines.append(line.lstrip(">").strip())

    return ParentNode("blockquote", text_to_leaf_nodes(" ".join(quote_lines)))


def md_ol_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    list_item_nodes = []
    for line in lines:
        txt = line[3:]  # example: 1. List Item 1
        list_item_nodes.append(ParentNode("li", text_to_leaf_nodes(txt)))

    return ParentNode("ol", list_item_nodes)


def md_ul_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    list_item_nodes = []
    for line in lines:
        txt = line[2:]  # example: * List Item 1
        list_item_nodes.append(ParentNode("li", text_to_leaf_nodes(txt)))

    return ParentNode("ul", list_item_nodes)
