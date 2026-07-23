from block_markdown import markdown_to_blocks, markdown_to_html_node
import os

def extract_title(markdown: str) -> str:
    blocks: list[str] = markdown_to_blocks(markdown)
    title: str = ""
    for block in blocks:
        if block.startswith("# "):
            title += block[2:]
            break
    if not title:
        raise Exception("Error: markdown doesn't have a title")
    return title


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        index_md = file.read()
    with open(template_path, "r") as file:
        template_html = file.read()
    # converting index.md to an html string
    index_html = markdown_to_html_node(index_md).to_html()
    title = extract_title(index_md)
    new_temp = template_html.replace("{{ Title }}", title).replace("{{ Content }}", index_html)
    with open(dest_path, "w") as file:
        file.write(new_temp)



