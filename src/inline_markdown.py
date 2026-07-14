import re
from textnode import TextNode, TextType

def split_nodes_delimiter(
        old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result = []
    for node in old_nodes:
        # if node.text_type is bold or italic or code, we're adding that as is
        # also if there's no delimiter present in the text, we also keep that as is
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            result.extend([node])
        else:
            split_list = node.text.split(delimiter)
            # all odd indices will be either be code or bold or italic no matter how many
            # instances of code or bold or italic the input textnode contains
            for index, value in enumerate(split_list):
                if index % 2 == 0:
                    result.extend([TextNode(value, node.text_type)])
                else:
                    result.extend([TextNode(value, text_type)])
            
    return result

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

 