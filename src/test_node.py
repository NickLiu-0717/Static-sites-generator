from htmlnode import HTMLNode
from leafnode import LeafNode
import unittest

class htmltest(unittest.TestCase):
    def test_props_to_html(self):
        prop = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }
        htmlnode = HTMLNode(None, None, None, prop)
        self.assertIsInstance(htmlnode, HTMLNode)
    
    def test_leafnode(self):
        test_cases = [("p", "This is a paragraph of text.",{"href": "https://www.google.com", "target": "_blank",})
                      ,("a", "Click me!", {"href": "https://www.google.com"})
                      ,(None, "This is a paragraph of text.")
                      ]
        for test_case in test_cases:
            leafnode = LeafNode(*test_case)
            self.assertIsInstance(leafnode, LeafNode)
    def not_leaf_test(self):
        leafnode = LeafNode("p", None, {"href": "https://www.google.com"})
        self.assertNotIsInstance(leafnode, LeafNode)
    
if __name__ == "__main__":
    # unittest.main()
    test_cases = [
        ("p", "This is a paragraph of text.",{"href": "https://www.google.com", "target": "_blank",})
        ,("a", "Click me!", {"href": "https://www.google.com"})
        ,(None, "This is a paragraph of text.")
        ,("p", "This is a paragraph of text.")
        ]
    for test_case in test_cases:
        leafnode = LeafNode(*test_case)
        print(leafnode.to_html())
  

    