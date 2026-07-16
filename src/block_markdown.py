from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST  = "unordered_list"
    OLIST = "ordered_list"
    FUCK = "fuck"

def markdown_to_blocks(markdown: str) -> list[str]:
    md_list = markdown.strip().split("\n\n")
    # this "if block" adds only the non-empty blocks
    return [block for block in md_list if block]

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # for code
    if lines[0].startswith("```") and len(lines) > 1 and lines[-1].endswith("```"):
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
    
    