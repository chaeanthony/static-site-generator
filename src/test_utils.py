import unittest

from utils import extract_markdown_images, extract_markdown_links
from markdownblock import (
    markdown_to_blocks,
    block_type_paragraph,
    block_type_olist,
    block_to_block_type,
    block_type_code,
    block_type_heading,
    block_type_quote,
    block_type_ulist,
)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_img(self):
        self.assertEqual(
            extract_markdown_images(
                "This is text with a ![image alt text](https://img.com/img) and ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [url text](url.com)"
            ),
            [
                ("image alt text", "https://img.com/img"),
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ],
        )

    def test_extract_link(self):
        self.assertEqual(
            extract_markdown_links(
                "This is text with a [image alt text](https://img.com/img) and ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
            ),
            [("image alt text", "https://img.com/img")],
        )


if __name__ == "__main__":
    unittest.main()
