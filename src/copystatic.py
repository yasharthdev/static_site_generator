import shutil
import os


def copy_all_content(source: str, destination: str) -> None:
    source_path = os.path.abspath(source)
    dest_path = os.path.abspath(destination)
    # removing the destination dir if it exists
    if os.path.exists(dest_path):
       shutil.rmtree(dest_path)
    # creating the destination now
    os.mkdir(dest_path)
    if os.path.exists(source_path):
        copy_tree(source_path, dest_path)

    return None

def copy_tree(src_path: str, dest_path: str) -> None:
    contents = os.listdir(src_path)
    for item in contents:
        # gotta get the item's path
        item_path = os.path.join(src_path, item)
        # if the item is a file, copy it directly to the destination folder
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_path)
        else:
            # item is a folder, pass it to the func again
            # first you join the item with the dest
            new_dest_path = os.path.join(dest_path, item)
            # then create that folder
            os.mkdir(new_dest_path)
            # pass it to the tree function
            copy_tree(item_path, new_dest_path)

    return None