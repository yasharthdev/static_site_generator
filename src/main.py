from copystatic import copy_all_content
from generate_page import generate_pages_recursive

def main():
    # copy content from static dir to public dir
    copy_all_content("static", "public")
    # generate html in public/ for every markdown file in content/ using template.html
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
