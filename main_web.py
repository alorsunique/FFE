from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from datetime import datetime
from pathlib import Path
import yaml


app = Flask(__name__)











def find_project_root(script_path, marker):
    current_path = script_path
    while not (current_path / marker).exists():
        # If block checks for parent of current path
        # If it cannot go up any further, base directory is reached
        if current_path.parent == current_path:
            raise FileNotFoundError(f"Could not find '{marker}' in any parent directories.")

        current_path = current_path.parent

    # If it exits the while loop, marker was found
    return current_path



def list_content(input_path, image_extension_dict):
    content_folder_list = []
    content_file_list = []

    for entry in input_path.iterdir():
        if entry.is_dir():
            content_folder_list.append(entry.relative_to(input_path))
        elif entry.is_file():
            # Check if the file is an image so that a thumbnail can be shown
            if entry.suffix in image_extension_dict:
                entry_dict = {
                    'name': entry.relative_to(input_path),
                    'parent_path': entry.parent,
                    'image_bool': True 
                }
            # If not, defaults to a default thumbnail
            else:
                entry_dict = {
                    'name': entry.relative_to(input_path),
                    'parent_path': entry.parent,
                    'image_bool': False 
                }
            content_file_list.append(entry_dict)

    return content_folder_list, content_file_list



def check_not_empty(folder_list, file_list):

    folder_check = False
    file_check = False

    if len(folder_list) > 0:
        folder_check = True
    if len(file_list) > 0:
        file_check = True

    if folder_check or file_check:
        whole_path_check = True
    else:
        whole_path_check = False

    check_not_empty_dict = {
        'whole_path_check': whole_path_check,
        'folder_check': folder_check,
        'file_check': file_check
    }

    return check_not_empty_dict


@app.route('/')
def index():
    # Current path will be an argument
    subpath = request.args.get("path", relative_home_path)
    print(f"Subpath: {subpath}")

    current_path = explorer_root / subpath
    current_path = current_path.resolve()
    print(f"Current Path: {current_path}")

    # This if statement makes sure that the explorer stays on the explorer root
    # This means it will stay in D
    if not str(current_path).lower().startswith(str(explorer_root).lower()):
        return redirect(url_for('index'))

    # Root Boolean will be used to determine whether the up button will be showed
    if current_path == explorer_root:
        root_boolean = True
        parent_path_string = ""
    else:
        root_boolean = False
        parent_path = current_path.relative_to(explorer_root).parent
        parent_path_string = str(parent_path).replace("\\", "/")

    print(f"Parent Path: {parent_path_string}")


    # Gather the content of the current path
    content_folder_list, content_file_list = list_content(current_path, image_extension)

    check_not_empty_dict = check_not_empty(content_folder_list, content_file_list)

    print(content_folder_list)

    return render_template(
        'index.html',
        index_folders=content_folder_list,
        index_files=content_file_list,
        index_current_path=str(current_path).replace("\\", "/"),
        index_parent_path=parent_path_string,
        index_root_check=root_boolean,
        index_home_path=home_path,
        index_check_not_empty_dict=check_not_empty_dict,
    )




# Return the path of the file
@app.route('/<path:file_path>')
def serve_file(file_path):
    full_path = (explorer_root / file_path).resolve()

    # Checks if the path is in D
    if not str(full_path).startswith(str(explorer_root)):
        return "Access Denied", 403

    return send_from_directory(full_path.parent, full_path.name)










@app.route('/sum_function/<a>+<b>')
def print_text(a,b):
    sum = int(a) + int(b)
    return str(sum)






if __name__ == '__main__':
    config_file_name = 'FFE_config.yaml'
    script_path = Path(__file__).resolve()
    project_dir = find_project_root(script_path, config_file_name)

    config_file_path = project_dir / config_file_name

    with open(config_file_path, "r") as open_config:
        config_content = yaml.safe_load(open_config)

    resources_dir = Path(config_content['resources_dir'])

    home_path = resources_dir.resolve()
    explorer_root = Path(home_path.drive + "\\") 

    print(f"Explorer Root: {explorer_root}")
    print(f"Home Path: {home_path}")

    relative_home_path = home_path.relative_to(explorer_root)
    
    print(f"Relative Home Path: {relative_home_path}")


    image_extension = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}


    # blacklist_path_list = [
        # WindowsPath('$RECYCLE.BIN'),
        # WindowsPath('System Volume Information')
    # ]

    app.run(debug=True)