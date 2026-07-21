from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST  = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    md_list = markdown.strip().split("\n\n")
    # this "if block" adds only the non-empty blocks as new lines become empty strings after
    # the split
    return [block for block in md_list if block]


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # for code
    if lines[0].startswith("```") and len(lines) > 1 and lines[-1].startswith("```"):
        return BlockType.CODE
    # for quote
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    # for unordered lists
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    is_ordered = True
    # for ordered lists
    for index, line in enumerate(lines, start=1):
        if not line.startswith(f"{index}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.OLIST
    return BlockType.PARAGRAPH             
            
    
def markdown_to_html_node(markdown: str) ->  ParentNode:
    nodes: list[HTMLNode] = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        # if there are multiple lines separated by \n (for quotes, lists, code)
        lines = block.split("\n")
        if block_type == BlockType.HEADING:
            hashes = 0
            for char in block:
                if char == "#":
                    hashes += 1
                else:
                    break
            children = text_to_html_node_children(block[hashes + 1:])
            nodes.append(ParentNode(f"h{hashes}", children))
        
        elif block_type == BlockType.PARAGRAPH:
            block_without_lines = block.replace("\n", " ")
            children = text_to_html_node_children(block_without_lines)
            nodes.append(ParentNode("p", children))

        elif block_type == BlockType.QUOTE:
            quote = " ".join([line[1:].strip() for line in lines])
            children = text_to_html_node_children(quote)
            nodes.append(ParentNode("blockquote", children))
            
        elif block_type == BlockType.ULIST:
            ul_items = []
            for line in lines:
                element = line[2:].strip()
                # for inline parsing of each element
                children = text_to_html_node_children(element)
                ul_items.append(ParentNode("li", children))
            nodes.append(ParentNode("ul", ul_items))
            
        elif block_type == BlockType.OLIST:
            ol_items = []
            for line in lines:
                # line.split(". ") = ["10", "buy **eggs**"], maxsplit required just in case
                # ". " is contained in the list itself
                element = line.split(". ", maxsplit=1)[1]
                children = text_to_html_node_children(element)
                ol_items.append(ParentNode("li", children))
            nodes.append(ParentNode("ol", ol_items))

        elif block_type == BlockType.CODE:
            # lines[1:-1] removes the ```, \n required for trailing new line according
            # to the instructions
            code = "\n".join(lines[1:-1]) + "\n" 
            code_children = TextNode(code, TextType.TEXT)
            html = text_node_to_html_node(code_children)
            code_block = ParentNode("code", [html])
            nodes.append(ParentNode("pre", [code_block]))

    return ParentNode("div", nodes)

        

def text_to_html_node_children(text: str) -> list[HTMLNode]:
    text_nodes: list[TextNode] = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(textnode) for textnode in text_nodes]
    return html_nodes
