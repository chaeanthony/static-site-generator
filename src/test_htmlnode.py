import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(str(HTMLNode("p", "text")), "HTMLNode(p, text, None, None)")

    def to_html(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode().to_html()

    def test_props_to_html(self):
        node = HTMLNode(
            "p",
            "text",
            None,
            {"href": "https://github.com/chaeanthony", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://github.com/chaeanthony" target="_blank"',
        )


class TestLeafNode(unittest.TestCase):
    def test_fields(self):
        node = LeafNode(
            "p",
            "lorem ipsum",
            {"href": "https://github.com/chaeanthony", "target": "_blank"},
        )
        self.assertTrue(node.tag == "p")
        self.assertTrue(node.value == "lorem ipsum")

    def test_to_html(self):
        self.assertEqual(
            LeafNode(
                "p", "lorem ipsum", {"href": "https://github.com/chaeanthony"}
            ).to_html(),
            '<p href="https://github.com/chaeanthony">lorem ipsum</p>',
        )

    def test_to_html_no_tag(self):
        self.assertEqual(
            LeafNode(
                None, "lorem ipsum", {"href": "https://github.com/chaeanthony"}
            ).to_html(),
            "lorem ipsum",
        )


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        div = ParentNode("div", [LeafNode("p", "child1"), LeafNode("p", "child2")])
        self.assertEqual("<div><p>child1</p><p>child2</p></div>", div.to_html())

    def test_to_html_nested_parents(self):
        div = ParentNode("div", [LeafNode("p", "child1"), LeafNode("p", "child2")])
        section = ParentNode(
            "section", [div, LeafNode("p", "child1"), LeafNode("p", "child2")]
        )
        self.assertEqual(
            "<section><div><p>child1</p><p>child2</p></div><p>child1</p><p>child2</p></section>",
            section.to_html(),
        )

    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, None).to_html()

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("p", None).to_html()


if __name__ == "__main__":
    unittest.main()
