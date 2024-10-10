from htmlnode import HTMLNode
# from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("parent nodes must have a tag")
        if self.children == None:
            raise ValueError("parent nodes must have a children")
        tmp_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            tmp_string += child.to_html()
        return tmp_string + f"</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
        