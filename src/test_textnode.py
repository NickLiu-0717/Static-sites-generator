import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is not a text node", "bold")
        self.assertNotEqual(node, node2)
    
    def test_URL(self):
        node = TextNode("This is a text node", "bold", None)
        self.assertIsInstance(node, TextNode)
    
    def test_diff_type(self):
        TYPE = ["bold", "Italic", "Blockquote"]
        for type in TYPE:
            self.assertIsInstance(TextNode("This is a text node", type), TextNode)

    def test_split_old_nodes(self):
        old1 = TextNode("**This is text with a ** bolded phrase in the middle", text_type_text)
        new1 = split_nodes_delimiter([old1], "**", text_type_bold)
        self.assertEqual(new1, [TextNode("This is text with a ", text_type_bold), TextNode(" bolded phrase in the middle", text_type_text)])
        
        old2 = [TextNode("This is text with a `bolded phrase` in the middle", text_type_text), TextNode("Happy yolo `hello world` in the peace", text_type_text)]
        new2 = split_nodes_delimiter(old2, "`", text_type_code)
        self.assertEqual(new2, [TextNode("This is text with a ", "text"), TextNode("bolded phrase", "code"), TextNode(" in the middle", "text"), TextNode("Happy yolo ", "text"), TextNode("hello world", "code"), TextNode(" in the peace", "text")])

        old3 = [TextNode("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", text_type_text)]
        new3 = split_nodes_delimiter(old3, "**", text_type_bold)
        self.assertEqual(new3, [TextNode("This is ", text_type_text), TextNode("text", text_type_bold), TextNode(" with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", text_type_text)])

        new4 = split_nodes_delimiter(new3, "*", text_type_italic)
        self.assertEqual(new4, [TextNode("This is ", text_type_text), TextNode("text", text_type_bold), TextNode(" with an ", text_type_text), TextNode("italic", text_type_italic), TextNode(" word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", text_type_text)])

        old5 = TextNode("This is text with a **bolded phrase** in the middle **and another bolded text** in the end", text_type_text)
        new5 = split_nodes_delimiter([old5], "**", text_type_bold)
        self.assertEqual(new5, [TextNode("This is text with a ", text_type_text), TextNode("bolded phrase", text_type_bold), TextNode(" in the middle ", text_type_text), TextNode("and another bolded text", text_type_bold), TextNode(" in the end", text_type_text)])
        
        old6 = TextNode("This is text with a **bolded phrase** in the middle and another bolded text **in the end**", text_type_text)
        new6 = split_nodes_delimiter([old6], "**", text_type_bold)
        self.assertEqual(new6, [TextNode("This is text with a ", text_type_text), TextNode("bolded phrase", text_type_bold), TextNode(" in the middle and another bolded text ", text_type_text), TextNode("in the end", text_type_bold)])
        
    def test_split_exception(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter([TextNode("This is text with a **bolded phrase** in the middle", text_type_text)], "!", text_type_bold)
            
    def test_extract_image_and_link(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        match = extract_markdown_images(text)
        self.assertEqual(match, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        match1 = extract_markdown_links(text)
        match2 = extract_markdown_images(text)
        self.assertEqual(match1, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
        self.assertEqual(match2, [])
        
        text = "[sdaf]ddgacvdfh [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and [to google](https://www.google.com)"
        match = extract_markdown_links(text)
        self.assertEqual(match, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev"), ("to google", "https://www.google.com")])
        
        text = "asdlfnhkasjdf asdjfhnaksj kjashdfkasjh"
        match = extract_markdown_images(text)
        self.assertEqual(match, [])
        
        text = "[sdaf]ddgacvdfh [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and [to boot dev](https://www.boot.dev)"
        match = extract_markdown_links(text)
        self.assertEqual(match, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev"), ("to boot dev", "https://www.boot.dev")])
        
    def test_split_nodes_image(self):
        node1 = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) hehe test 1 2 3.", text_type_text, None)
        new_nodes = split_nodes_image([node1])
        self.assertEqual(new_nodes, [TextNode("This is text with a ", text_type_text), TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" hehe test 1 2 3.", text_type_text)])
        
        node2 = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)
        new_nodes = split_nodes_image([node2])
        self.assertEqual(new_nodes, [TextNode("This is text with a ", text_type_text, None), TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", text_type_text, None), TextNode("obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg")])

        node3 = [node1, node2]
        new_nodes = split_nodes_image(node3)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", text_type_text, None), TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" hehe test 1 2 3.", text_type_text, None), TextNode("This is text with a ", text_type_text, None), TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", text_type_text, None), TextNode("obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg")])
        
        node4 = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", text_type_text)
        new_nodes = split_nodes_image([node4])
        self.assertEqual(new_nodes, [TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", text_type_text), TextNode("obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg")])
        
    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [TextNode("This is text with a link ", text_type_text, None), TextNode("to boot dev", text_type_link, "https://www.boot.dev"), TextNode(" and ", text_type_text, None), TextNode("to youtube", text_type_link, "https://www.youtube.com/@bootdotdev")])
    
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and an image ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [TextNode("This is text with a link ", text_type_text, None), TextNode("to boot dev", text_type_link, "https://www.boot.dev"), TextNode(" and an image ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type_text, None)])

    def test_text_to_textnode(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        exp_output = [
                        TextNode("This is ", text_type_text),
                        TextNode("text", text_type_bold),
                        TextNode(" with an ", text_type_text),
                        TextNode("italic", text_type_italic),
                        TextNode(" word and a ", text_type_text),
                        TextNode("code block", text_type_code),
                        TextNode(" and an ", text_type_text),
                        TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", text_type_text),
                        TextNode("link", text_type_link, "https://boot.dev"),
                    ]
        self.assertEqual(nodes, exp_output)
        
        text = "This is **bold text** with an *italic* word **another bold text** and a `code block` and *another italic text* and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        exp_output = [
                        TextNode("This is ", text_type_text),
                        TextNode("bold text", text_type_bold),
                        TextNode(" with an ", text_type_text),
                        TextNode("italic", text_type_italic),
                        TextNode(" word ", text_type_text),
                        TextNode("another bold text", text_type_bold),
                        TextNode(" and a ", text_type_text),
                        TextNode("code block", text_type_code),
                        TextNode(" and ", text_type_text),
                        TextNode("another italic text", text_type_italic),
                        TextNode(" and an ", text_type_text),
                        TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", text_type_text),
                        TextNode("link", text_type_link, "https://boot.dev"),
                    ]
        self.assertEqual(nodes, exp_output)

        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) [This is https://fakelink.com] **text** with an *italic* word and a **code block** and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        exp_output = [
                        TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" [This is https://fakelink.com] ", text_type_text),
                        TextNode("text", text_type_bold),
                        TextNode(" with an ", text_type_text),
                        TextNode("italic", text_type_italic),
                        TextNode(" word and a ", text_type_text),
                        TextNode("code block", text_type_bold),
                        TextNode(" and an ", text_type_text),
                        TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", text_type_text),
                        TextNode("link", text_type_link, "https://boot.dev"),
                    ]
        self.assertEqual(nodes, exp_output)
        
    def test_markdown_to_blocks(self):
        markdown = "# This is heading\n\nThis is a paragraph\n\n* This is first list\n* This is second list"
        list = markdown_to_blocks(markdown)
        self.assertEqual(list, ["# This is heading", "This is a paragraph", "* This is first list\n* This is second list"])
        
        markdown = "# This is heading   \n\n  This is a paragraph  \n\n* This is first list   \n* This is second list  "
        list = markdown_to_blocks(markdown)
        self.assertEqual(list, ["# This is heading", "This is a paragraph", "* This is first list   \n* This is second list"])
        
        markdown = "\n# This is heading\n\nThis is a paragraph\n\n* This is first list\n* This is second list"
        list = markdown_to_blocks(markdown)
        self.assertEqual(list, ["# This is heading", "This is a paragraph", "* This is first list\n* This is second list"])
        
        markdown = "# This is heading\n\nThis is a paragraph\n\n* This is first list\n* This is second list\n"
        list = markdown_to_blocks(markdown)
        self.assertEqual(list, ["# This is heading", "This is a paragraph", "* This is first list\n* This is second list"])
        
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
        
        
if __name__ == "__main__":
    unittest.main()
    # markdown = "# This is heading   \n\n  This is a paragraph  \n\n* This is first list   \n  * This is second list  "
    # list = markdown_to_blocks(markdown)
    # print(list)