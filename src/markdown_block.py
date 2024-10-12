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

def block_to_block_type(block_of_markdown):
    sections = block_of_markdown.split("\n")
    if block_of_markdown[:2] == "# " or block_of_markdown[:3] == "## " or block_of_markdown[:4] == "### " or block_of_markdown[:5] == "#### " or block_of_markdown[:6] == "##### " or block_of_markdown[:7] == "###### ":
        return "heading"
    elif block_of_markdown[:3] == "```" and block_of_markdown[-3:] == "```":
        return "code"
    elif block_of_markdown[0] == ">":
        for line in sections:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    elif block_of_markdown[:2] == "* " or block_of_markdown[:2] == "- ":
        for line in sections:
            if block_of_markdown[:2] == "* ":
                if not line.startswith("* "):
                    return "paragraph"
            elif block_of_markdown[:2] == "- ":
                if not line.startswith("- "):
                    return "paragraph"
        return "unordered_list"
    elif block_of_markdown[:3] == "1. ":
        correct = 1
        for i in range(len(sections)-1):
            if sections[i+1][:3] == f"{i+2}. ":
                correct += 1
        if correct == len(sections):
            return "ordered_list"
        else:
            return "paragraph"
    else:
        return "paragraph"
    
def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise Exception("No h1 header found")