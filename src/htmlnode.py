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

