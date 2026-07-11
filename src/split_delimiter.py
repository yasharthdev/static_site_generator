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
            # all odd indices will be code no matter how many instances of code
            # the input textnode contains
            for index, value in enumerate(split_list):
                if index % 2 == 0:
                    result.extend([TextNode(value, node.text_type)])
                else:
                    result.extend([TextNode(value, text_type)])
            
    return result

# node = TextNode("This is a text with a `code` block", TextType.TEXT)
# old_nodes = [
#     TextNode("This is ", TextType.TEXT),
#     TextNode("already bold", TextType.BOLD),
#     TextNode(" and this has `code` and more `code` in it", TextType.TEXT),
# ]
# more_nodes = [
#             TextNode("This is", TextType.TEXT),
#             TextNode("some already italic", TextType.ITALIC),
#             TextNode("and **lots and lots** of **large** bold text", TextType.TEXT),
#             TextNode("and some more code for fun", TextType.CODE)
#         ]
# print(split_nodes_delimiter(more_nodes, "**", TextType.BOLD))


 