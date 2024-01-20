import argparse
import os
import yaml

DEFAULT_YAML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'project_structure.yaml')

def get_default_yaml() -> None:
    """
    Print the content of the default YAML file.

    Returns:
        None
    """
    try:
        with open(DEFAULT_YAML_PATH, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: YAML file not found at {DEFAULT_YAML_PATH}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")

def create_structure(path:str, structure:dict) -> None:
    """
    Create directory structure based on the provided dictionary.

    Args:
        path (str): The current path where the structure is being created.
        structure (dict): Dictionary representing the structure to be created.
    """
    for entry in structure:
        entry_name = entry.get('name')
        entry_type = entry.get('type')
        entry_content = entry.get('content', [])
        entry_file_content = entry.get('content', '')

        current_path = os.path.join(path, entry_name)

        if entry_type == 'directory':
            os.makedirs(current_path, exist_ok=True)
            if entry_content:
                create_structure(current_path, entry_content)
        elif entry_type == 'file':
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path, entry_name), 'w') as file:
                file.write(entry_file_content or '')
        else:
            raise ValueError("Error: Invalid entry type")

def project_build(path:str, yaml_path:str = DEFAULT_YAML_PATH) -> None:
    """
    Build the project directory structure.

    Args:
        path (str): The root path where the project structure will be created.
        yaml_path (str, optional): Path to the YAML file containing the project structure definition. Defaults to DEFAULT_YAML_PATH.
    """
    if os.path.exists(path):
        raise FileExistsError(f"Error: The specified root directory '{path}' already exists.")
    
    try:
        with open(yaml_path, 'r') as file:
            structure = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: YAML file not found at {yaml_path}")
    
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred: {e}")
    
    create_structure(path, structure['project_structure'])    
    

def main():
    parser = argparse.ArgumentParser(description='Create a directory structure based on the project_structure.yaml file.')
    parser.add_argument('-p', '--path', type=str, default='.', dest='path_of_project', help='Path where the parent directory of the project will be set.')
    parser.add_argument('-n', '--name', type=str, help='Name of the project and the root folder.')
    parser.add_argument('--set-yaml', type=str, default=DEFAULT_YAML_PATH, help='Path to the YAML file containing the project structure definition. Default is an internal project_structure.yaml.')
    parser.add_argument('--yaml', action='store_true', help='Path to the YAML file containing the project structure definition. If provided, print the content of the YAML file and exit.')
    
    args = parser.parse_args()
    
    if args.yaml:
        get_default_yaml()
        return
    
    if args.name is None:
        print("Error: --name is required when not using --yaml.")
        return
    
    project_path = os.path.join(args.path_of_project, args.name)
    
    try:
        project_build(project_path, yaml_path=args.set_yaml)
        print(f"Project structure created successfully at '{project_path}'.")
    except Exception as e:
        print(f"Error: Failed to create project structure: {e}")

if __name__ == '__main__':
    main()
