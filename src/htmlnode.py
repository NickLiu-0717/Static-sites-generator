class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("wait to be overrided")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        attri = []
        for key in self.props:
            attri.append(f' {key}="{self.props[key]}"')
        return "".join(attri)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError("ERROR: Leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("ERROR: Parent nodes must have a tag")
        if self.children == None:
            raise ValueError("ERROR: Parent nodes must have a children")
        tmp_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            tmp_string += child.to_html()
        return tmp_string + f"</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"