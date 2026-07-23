from copystatic import copy_all_content
from generate_page import generate_page

def main():
    # copy content from static dir to public dir
    copy_all_content("static", "public")
    # generate html from markdown
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()





    



