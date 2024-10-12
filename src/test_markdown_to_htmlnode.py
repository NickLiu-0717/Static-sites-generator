import unittest
from markdown_to_htmlnode import *

class TestMarkdownToHTMLnode(unittest.TestCase):
    def test_heading_to_html(self):
        block = "# This is a heading 1"
        htmlnode = heading_to_htmlnode(block)
        self.assertEqual(htmlnode.__repr__(), 'ParentNode(h1, [LeafNode(None, This is a heading 1, None)], None)')
        
        block = "# This is a **heading 1**"
        htmlnode = heading_to_htmlnode(block)
        self.assertEqual(htmlnode.__repr__(), 'ParentNode(h1, [LeafNode(None, This is a , None), LeafNode(b, heading 1, None)], None)')
        
        block = "### This is a **heading 3** and a *italic word*"
        htmlnode = heading_to_htmlnode(block)
        self.assertEqual(htmlnode.__repr__(), 'ParentNode(h3, [LeafNode(None, This is a , None), LeafNode(b, heading 3, None), LeafNode(None,  and a , None), LeafNode(i, italic word, None)], None)')

    # def test_quote_to_html(self):
    #     block = ">This is a random quote message"
    #     htmlnode = quote_to_htmlnode(block)
    #     self.assertEqual(htmlnode.__repr__(), ParentNode("blockquote", [ParentNode("p", [LeafNode(None, "This is a random quote message")])]).__repr__())
        
    #     block = ">This is a random quote message\n>This is another random quote message"
    #     htmlnode = quote_to_htmlnode(block)
    #     self.assertEqual(htmlnode.__repr__(), ParentNode("blockquote", [ParentNode("p", [LeafNode(None, "This is a random quote message\nThis is another random quote message")])]).__repr__())

    #     block = ">This is a **random** quote message"
    #     htmlnode = quote_to_htmlnode(block)
    #     self.assertEqual(htmlnode.__repr__(), ParentNode("blockquote", [ParentNode("p", [LeafNode(None, "This is a "), LeafNode("b", "random"), LeafNode(None, " quote message")])]).__repr__())

    #     block = ">This is a **random** quote message\n>This is another *italic* quote"
    #     htmlnode = quote_to_htmlnode(block)
    #     self.assertEqual(htmlnode.__repr__(), ParentNode("blockquote", [ParentNode("p", [LeafNode(None, "This is a "), LeafNode("b", "random"), LeafNode(None, " quote message\nThis is another "), LeafNode("i", "italic"), LeafNode(None, " quote")])]).__repr__())

    def test_paragraph_to_htmlnode(self):
        para = "asdfasg asdfasdg asdgoiih sdflkl #asdfag"
        htmlnode = paragraph_to_htmlnode(para)
        self.assertEqual(htmlnode.__repr__(), ParentNode("p", [LeafNode(None, "asdfasg asdfasdg asdgoiih sdflkl #asdfag")]).__repr__())
        
    def test_code_to_htmlnode(self):
        block = "```random code right here```"
        htmlnode = code_to_htmlnode(block)
        self.assertEqual(htmlnode.__repr__(), ParentNode("pre", [ParentNode("code", [LeafNode(None, "random code right here")])]).__repr__())
        
    def test_list_to_htmlnode(self):
        block = "* first item\n* second item\n* third item"
        htmlnode = list_to_htmlnode(block)
        self.assertEqual(htmlnode.__repr__(), ParentNode("ul", [ParentNode("li", [LeafNode(None, "first item")]), ParentNode("li", [LeafNode(None, "second item")]), ParentNode("li", [LeafNode(None, "third item")])]).__repr__())
        
        block = "1. first item\n2. second item\n3. third item"
        htmlnode = list_to_htmlnode(block)
        self.assertEqual(htmlnode.__repr__(), ParentNode("ol", [ParentNode("li", [LeafNode(None, "first item")]), ParentNode("li", [LeafNode(None, "second item")]), ParentNode("li", [LeafNode(None, "third item")])]).__repr__())

    def test_markdown_to_html_node(self):
        para = "asdfasg asdfasdg asdgoiih sdflkl #asdfag"
        htmlnode = markdown_to_html_node(para)
        self.assertEqual(htmlnode.__repr__(), ParentNode("div", [ParentNode("p", [LeafNode(None, "asdfasg asdfasdg asdgoiih sdflkl #asdfag")])]).__repr__())
        
        markdown = "# This is heading\n\nThis is a paragraph\n\n* This is first list\n* This is second list"

if __name__ == "__main__":
    unittest.main()
    markdown = "# This is heading\n\n```This is a code```\n\n1. This is first list\n2. This is second list\n"
    htmlnode = markdown_to_html_node(markdown)
    print(htmlnode.__repr__())