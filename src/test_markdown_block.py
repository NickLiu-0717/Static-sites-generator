import unittest
from markdown_block import *

class test_markdown(unittest.TestCase):
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
        
        markdown = "# This is heading\n\n```This is a code```\n\n1. This is first list\n2. This is second list\n"
        list = markdown_to_blocks(markdown)
        self.assertEqual(list, ["# This is heading", "```This is a code```", "1. This is first list\n2. This is second list"])
        
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
        
    def test_block_to_block_type(self):
        block = "## This is a heading"
        type = block_to_block_type(block)
        self.assertEqual(type, "heading")
        
        block = "```\nThis is a code\n```"
        type = block_to_block_type(block)
        self.assertEqual(type, "code")
        
        block = "``` This is not a code "
        type = block_to_block_type(block)
        self.assertEqual(type, "paragraph")
        
        block = "1. asdfasg\n2. fedghakgfha\n3. asdgfoag"
        type = block_to_block_type(block)
        self.assertEqual(type, "ordered_list")
        
        block = "1.asdfasg\n2.fedghakgfha\n3.asdgfoag"
        type = block_to_block_type(block)
        self.assertEqual(type, "paragraph")
        
        block = "* asdfasg\n* fedghakgfha\n* asdgfoag"
        type = block_to_block_type(block)
        self.assertEqual(type, "unordered_list")
        
        block = "*asdfasg\n*fedghakgfha\n*asdgfoag"
        type = block_to_block_type(block)
        self.assertEqual(type, "paragraph")
        
        block = "1. asdfasg\n2. fedghakgfha\n4. asdgfoag"
        type = block_to_block_type(block)
        self.assertEqual(type, "paragraph")
        
        block = "asdfasg\n2. fedghakgfha\nasdgfoag"
        type = block_to_block_type(block)
        self.assertEqual(type, "paragraph")
        
        block = "##This is a heading"
        type = block_to_block_type(block)
        self.assertEqual(type, "paragraph")
        
        block = "###### This is a heading"
        type = block_to_block_type(block)
        self.assertEqual(type, "heading")
        
        block = "####### This is a heading"
        type = block_to_block_type(block)
        self.assertEqual(type, "paragraph")
        
        block = "* asdfasg\n- fedghakgfha\n* asdgfoag"
        type = block_to_block_type(block)
        self.assertEqual(type, "paragraph")
        
        block = "```This is a code```"
        type = block_to_block_type(block)
        self.assertEqual(type, "code")
if __name__ == "__main__":
    unittest.main()