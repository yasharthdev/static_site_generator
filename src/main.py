from copystatic import copy_all_content
from generate_page import generate_pages_recursive
import sys

def main():
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    else:
        baespath = "/"
    # copy content from static dir to public dir
    copy_all_content("static", "docs")
    # generate html in public/ for every markdown file in content/ using template.html
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
