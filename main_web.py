from flask import Flask, render_template, request, url_for, redirect, send_from_directory, jsonify
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



def list_content(input_path, image_extension_dict, video_extension_dict):
    content_folder_list = []
    content_file_list = []

    for entry in input_path.iterdir():
        if entry.is_dir():
            content_folder_list.append(entry.relative_to(input_path))
        elif entry.is_file():
            # Check if the file is an image so that a thumbnail can be shown
            if entry.suffix.lower() in image_extension_dict:
                entry_dict = {
                    'name': entry.relative_to(input_path),
                    'parent_path': entry.parent,
                    'image_bool': True,
                    'video_bool': False
                }
            # Check if the file is a video so that a thumbnail can be shown
            elif entry.suffix.lower() in video_extension_dict:
                entry_dict = {
                    'name': entry.relative_to(input_path),
                    'parent_path': entry.parent,
                    'image_bool': False,
                    'video_bool': True
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


# This function checks if the folder list and the file list has content
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
    # address_bar_path is the path in the address bar
    # If empty, it will default to the home_path
    address_bar_path = request.args.get("path", home_path)
    print(f"Address Bar Path: {address_bar_path}")

    current_path = Path(address_bar_path).resolve()

    if not current_path.exists():
        print('Path not found')
        return redirect(url_for('index'))

    # Here current_path is converted to string so that 
    # it can be stored properly in HTML
    current_path_string = str(current_path).replace("\\", "/")

    # root_boolean will be used to determine whether the up button will be shown
    if str(current_path) == f'{current_path.drive}\\':
        root_boolean = True
        # If at the root of the drive, parent_path should be empty
        parent_path_string = ""
    else:
        root_boolean = False
        parent_path = current_path.parent
        # parent_path is converted to string
        parent_path_string = str(parent_path).replace("\\", "/")

    print(f"Parent Path: {parent_path_string}")

    # Gather the content of the current path
    content_folder_list, content_file_list = list_content(current_path, image_extension, video_extension)

    check_not_empty_dict = check_not_empty(content_folder_list, content_file_list)

    return render_template(
        'index.html',
        index_folders=content_folder_list,
        index_files=content_file_list,
        index_current_path=current_path_string,
        index_parent_path=parent_path_string,
        index_root_check=root_boolean,
        index_home_path=home_path,
        index_check_not_empty_dict=check_not_empty_dict,
    )




# Return the path of the file
@app.route('/<path:file_path>')
def serve_file(file_path):
    full_path = Path(file_path).resolve()
    # First argument is where it will look for the second argument
    return send_from_directory(full_path.parent, full_path.name)














@app.route('/export_selection', methods=['POST'])
def export_selection():
    try:
        data = request.get_json()
        selected = data.get('selected', [])
        print("HEYS")
        export_path = selection_dir / "Out.json"  # You can change this path
        print(export_path)
        with open(export_path, 'w', encoding='utf-8') as f:
            import json
            json.dump(selected, f, indent=4)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Export Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500



@app.route('/get_change_drive', methods=['POST'])
def get_change_drive():
    data = request.get_json()
    print(data)
    return jsonify({"status": "success"}), 200




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
    print(f"Home Path: {home_path}")

    current_path = home_path
    print(f"Current Path: {current_path}")

    selection_dir = resources_dir / "Exported Selection"

    image_extension = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
    video_extension = {'.mp4', '.mov', '.webm', '.avi'}

    app.run(debug=True, port=1080)