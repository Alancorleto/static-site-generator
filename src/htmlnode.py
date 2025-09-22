from textnode import TextNode, TextType


class HTMLNode:    
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")


    def props_to_html(self):
        if not self.props:
            return ""
        
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        
        return props_str


    def __repr__(self):
        return f"[HTMLNode]\ntag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props})"



class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("LeafNode must have a value to convert to HTML")
        if not self.tag:
            return self.value
        
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    

    def __repr__(self):
        return f"[LeafNode]\ntag: {self.tag}\nvalue: {self.value}\nprops: {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    

    def to_html(self) -> str:
        if not self.children:
            raise ValueError("ParentNode must have children to convert to HTML")
        if not self.tag:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        
        props_str = self.props_to_html()
        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"
    

    def __repr__(self):
        return f"[ParentNode]\ntag: {self.tag}\nchildren: {self.children}\nprops: {self.props})"



def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        if not text_node.url:
            raise ValueError("Link TextNode must have a URL to convert to HTML")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("Image TextNode must have a URL to convert to HTML")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unknown TextType: {text_node.text_type}")
