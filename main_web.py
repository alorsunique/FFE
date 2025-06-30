from flask import Flask, render_template, request, url_for, redirect
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



def list_content(input_path):
    content_folder_list = []
    content_file_list = []

    for entry in input_path.iterdir():
        if entry.is_dir():
            content_folder_list.append(entry.relative_to(input_path))
        elif entry.is_file():
            content_file_list.append(entry.relative_to(input_path))

    return content_folder_list, content_file_list



@app.route('/')
def index():
    subpath = request.args.get("path", "")
    print(f"Subpath: {subpath}")
    current_path = (explorer_root / subpath).resolve()
    print(f"Current Path: {current_path}")
    print(f"Explorer Root: {explorer_root}")


    # Block escaping the drive root (D:\)
    if not str(current_path).lower().startswith(str(explorer_root).lower()):
        return redirect(url_for('index'))

    rel_path = current_path.relative_to(explorer_root)


    content_folder_list, content_file_list = list_content(current_path)
    
    if current_path == explorer_root:
        root_boolean = True
    else:
        root_boolean = False

    parent_path = "" if root_boolean else str(rel_path.parent).replace("\\", "/")

    return render_template(
        'index.html',
        folders=content_folder_list,
        files=content_file_list,
        current_path=str(rel_path).replace("\\", "/"),
        parent_path=parent_path,
        is_at_root=root_boolean,
        home_path=home_path
    )

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

    current_path = home_path


    app.run(debug=True)