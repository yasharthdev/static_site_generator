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

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        rem_text = node.text
        matches = extract_markdown_images(rem_text)
        # no matches found, meaning no images in the node, return as is
        if not matches:
            result.extend([node])
        else:
            for alt, img_link in matches:
                sections = rem_text.split(f"![{alt}]({img_link})", 1)
                # if first element is text, second will be an image, text added
                # conditionally, image added regardless
                if sections[0]:
                    result.append(TextNode(sections[0], TextType.TEXT))
                result.append(TextNode(alt, TextType.IMAGE, img_link))
                rem_text = sections[1]
            # if there's still text remaining, add it to the result as TextType.TEXT
            if rem_text:
                result.extend([TextNode(rem_text, TextType.TEXT)])

    return result

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        rem_text = node.text
        matches = extract_markdown_links(rem_text)
        # no matches found, meaning no links in the node, return as is
        if not matches:
            result.extend([node])
        else:
            for anchor, link in matches:
                sections = rem_text.split(f"[{anchor}]({link})", 1)
                # if first element is text, second will be a link, text added
                # conditionally, link added regardless 
                if sections[0]:
                    result.append(TextNode(sections[0], TextType.TEXT))
                result.append(TextNode(anchor, TextType.LINK, link))
                rem_text = sections[1]
            # if there's still text remaining, add it to the result as TextType.TEXT
            if rem_text:
                result.extend([TextNode(rem_text, TextType.TEXT)])

    return result

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
