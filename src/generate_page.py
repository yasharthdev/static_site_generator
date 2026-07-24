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

def generate_pages_recursive(
        dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    content_items = os.listdir(dir_path_content) # ["content", "blog", "index.md"]
    for item in content_items:
        item_source_path = os.path.join(dir_path_content, item)
        item_dest_path = os.path.join(dest_dir_path, item)
        # splitting the file with ".", last element will be the extension (markdown here)
        if os.path.isfile(item_source_path) and item.split(".")[-1] == "md":
            # makes sure that the copied file is index.html instead of index.md
            item_dest_path_html = item_dest_path.replace(".md", ".html")
            generate_page(item_source_path, template_path, item_dest_path_html)
        else:
            os.mkdir(item_dest_path)
            generate_pages_recursive(item_source_path, template_path, item_dest_path)

