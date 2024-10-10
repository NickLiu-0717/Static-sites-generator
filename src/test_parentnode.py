from parentnode import ParentNode
from leafnode import LeafNode
import unittest

class parentnodetest(unittest.TestCase):
    def test_repr(self):
        test_case = (
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        node = ParentNode(*test_case)
        self.assertEqual(node.__repr__(), "ParentNode(p, [LeafNode(b, Bold text, None), LeafNode(None, Normal text, None), LeafNode(i, italic text, None), LeafNode(None, Normal text, None)], None)")
        
    def test_values(self):
        node = ParentNode("b", LeafNode("i", "Hello World", {"class": "primary"}))
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.children.__repr__(), LeafNode("i", "Hello World", {"class": "primary"}).__repr__())
        
    def test_to_html(self):
        node1 = ParentNode("b", [LeafNode("i", "Hello World")], {"href": "https://www.google.com"})
        self.assertEqual(node1.to_html(), '<b href="https://www.google.com"><i>Hello World</i></b>')
        
        node2 = ParentNode("b", [LeafNode("i", "Hello World", {"class": "primary"})], {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), '<b href="https://www.google.com"><i class="primary">Hello World</i></b>')
        
        node3 = ParentNode("b", [LeafNode("i", "Hello World"), LeafNode("a", "random text here")])
        self.assertEqual(node3.to_html(), '<b><i>Hello World</i><a>random text here</a></b>')
        
        node4 = ParentNode("p",[LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
        self.assertEqual(node4.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
        node5 = ParentNode("div", [node4])
        self.assertEqual(node5.to_html(), '<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>')
        
    
    
if __name__ == "__main__":
    unittest.main()
    # test_case = (
    #         "p",
    #         [
    #             LeafNode("b", "Bold text"),
    #             LeafNode(None, "Normal text"),
    #             LeafNode("i", "italic text"),
    #             LeafNode(None, "Normal text"),
    #         ]
    #     )
    # node = ParentNode(*test_case)
    # print(node)
    # node1 = ParentNode("b", [LeafNode("i", "Hello World")], {"href": "https://www.google.com"})
    # print(node1.to_html())
    # node3 = ParentNode("b", [LeafNode("i", "Hello World"), LeafNode("a", "random text here")])
    # print(node3.to_html())