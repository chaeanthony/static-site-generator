class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""
        res = ""
        for key, val in self.props.items():
            res += f' {key}="{val}"'

        return res


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        # if not self.value:
        #     raise ValueError("Value is required for leaf nodes")
        if not self.tag:
            return self.value

        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

    def to_html(self):
        if not self.tag:
            raise ValueError("Invalid HTML: no tag")
        if not self.children:
            raise ValueError("Invalid HTML: no children html")

        res = ""
        for node in self.children:
            if isinstance(node, LeafNode):
                try:
                    res += node.to_html()
                except ValueError as ve:
                    print(
                        f"ParentNode.to_html(): Error converting html node to html.\nNode: {str(node)}\nError: {ve}"
                    )
                except Exception as e:
                    print(e)

            elif isinstance(node, ParentNode):
                res += node.to_html()

            else:
                raise Exception("Invalid node type")

        return f"<{self.tag}{self.props_to_html()}>{res}</{self.tag}>"
