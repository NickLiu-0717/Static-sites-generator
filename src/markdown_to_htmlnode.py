from htmlnode import *
from textnode import *
from markdown_block import *




def define_heading_tag_with_text(heading_block):
    if heading_block[:2] == "# ":
        return "h1", heading_block[2:]
    elif heading_block[:3] == "## ":
        return "h2", heading_block[3:]
    elif heading_block[:4] == "### ":
        return "h3", heading_block[4:]
    elif heading_block[:5] == "#### ":
        return "h4", heading_block[5:]
    elif heading_block[:6] == "##### ":
        return "h5", heading_block[6:]
    elif heading_block[:7] == "###### ":
        return "h6", heading_block[7:]

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, textnodes))

def heading_to_htmlnode(block):
    heading_tag, heading_text = define_heading_tag_with_text(block)
    return ParentNode(heading_tag, text_to_children(heading_text))

def quote_to_htmlnode(block):
    sections = block.split("\n")
    quote_text_list = list(map(lambda text: text[1:], sections))
    quote_text = "\n".join(quote_text_list)
    child_of_quote = [ParentNode("p", text_to_children(quote_text))]
    return ParentNode("blockquote", child_of_quote)

def paragraph_to_htmlnode(block):
    lines = block.split('\n')
    paragraph = " ".join(lines)
    return ParentNode("p", text_to_children(paragraph))

def code_to_htmlnode(block):
    code_text = block.strip("`")
    return ParentNode("pre", [ParentNode("code", text_to_children(code_text))])

def list_to_htmlnode(block):
    sections = block.split("\n")
    type = block_to_block_type(block)
    if type == "unordered_list":
        text_list = list(map(lambda text: text[2:], sections))
        tag = "ul"
    elif type == "ordered_list":
        text_list = list(map(lambda text: text[3:], sections))
        tag = "ol"
    li_nodes = []
    for text in text_list:
        li_nodes.append(ParentNode("li", text_to_children(text)))
    return ParentNode(tag, li_nodes)

block_type_to_function = {
                "quote": quote_to_htmlnode, 
                "unordered_list": list_to_htmlnode, 
                "ordered_list": list_to_htmlnode,
                "code": code_to_htmlnode, 
                "paragraph": paragraph_to_htmlnode,
                "heading": heading_to_htmlnode
                } 

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        nodes.append(block_type_to_function[block_type](block))
    return ParentNode("div", nodes)
      