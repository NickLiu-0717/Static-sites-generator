from leafnode import LeafNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"
all_type = {"**", "*", "`"}

class TextNode:
    def __init__(self, TEXT, text_type, URL=None):
        self.text = TEXT
        self.text_type = text_type
        self.url = URL
        
    def __eq__(self, textnode):
        if self.text == textnode.text and self.text_type == textnode.text_type and self.url == textnode.url:
            return True
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(textnode):
    if textnode.text_type == "text":
        return LeafNode(None, textnode.text)
    elif textnode.text_type == "bold":
        return LeafNode("b", textnode.text)
    elif textnode.text_type == "italic":
        return LeafNode("i", textnode.text)
    elif textnode.text_type == "code":
        return LeafNode("code", textnode.text)
    elif textnode.text_type == "link":
        return LeafNode("a", textnode.text, {"href":textnode.url})
    elif textnode.text_type == "image":
        return LeafNode("img", "", {"src":textnode.url, "alt":textnode.text})
    else:
        raise Exception("Invalid text type")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    if delimiter not in all_type:
        raise Exception("Invalid Markdown syntax")
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_node_list.append(node)
            continue
        text_list = node.text.split(delimiter)
        if len(text_list) > 1:
            for i in range(len(text_list)):
                if i % 2 == 0:
                    if text_list[i] != "":
                        new_node_list.append(TextNode(text_list[i], text_type_text))
                else:
                    new_node_list.append(TextNode(text_list[i], text_type))
        else:
            new_node_list.append(node)
    return new_node_list

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extract_images = extract_markdown_images(node.text)
        if len(extract_images) == 0:
            new_nodes.append(node)
            continue
        sections = ["", node.text]
        for image in extract_images:
            image_alt, image_link = image
            sections = sections[1].split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(image_alt, text_type_image, image_link))

        if sections[1] != "":
            new_nodes.append((TextNode(sections[1], text_type_text)))
    return new_nodes
    
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extract_links = extract_markdown_links(node.text)
        if len(extract_links) == 0:
            new_nodes.append(node)
            continue
        sections = ["", node.text]
        for link in extract_links:
            link_alt, url = link
            sections = sections[1].split(f"[{link_alt}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link_alt, text_type_link, url))

        if sections[1] != "":
            new_nodes.append((TextNode(sections[1], text_type_text)))
    return new_nodes      
    
def extract_markdown_images(text): 
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    bold_nodes = split_nodes_delimiter([node], "**", text_type_bold)
    itatlic_nodes = split_nodes_delimiter(bold_nodes, "*", text_type_italic)
    code_nodes = split_nodes_delimiter(itatlic_nodes, "`", text_type_code)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)
    return link_nodes

def markdown_to_blocks(markdown):
    block_list = []
    strip_markdown = markdown.strip("\n")
    blocks = strip_markdown.split("\n\n", 1)
    block_list.append(blocks[0].strip())
    if len(blocks) != 1:
        if blocks[1][:2] == "\n":
            blocks[1] = blocks[1].strip("\n")
        block_list += markdown_to_blocks(blocks[1])
    return block_list