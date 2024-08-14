import os
import shutil
import sys
from pathlib import Path

def create_django_project():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <project_name>")
        sys.exit(1)
    
    project_name = sys.argv[1]

    placeholder = "project-name-placeholder"
    template_dir = "project-template"
    project_dir = Path(project_name) / project_name

    # Create Django project
    os.system(f"django-admin startproject {project_name}")

    # Check if the template directory exists
    if not Path(template_dir).exists():
        print(f"Template directory '{template_dir}' does not exist.")
        sys.exit(1)

    # Copy custom settings.py and urls.py into the project folder
    shutil.copy(Path(template_dir) / "project" / "settings.py", project_dir / "settings.py")
    shutil.copy(Path(template_dir) / "project" / "urls.py", project_dir / "urls.py")

    # Copy everything else except the project folder into the project root
    for item in Path(template_dir).rglob('*'):
        if item.is_file():
            shutil.copy(item, Path(project_name) / item.relative_to(template_dir))
        elif item.is_dir():
            os.makedirs(Path(project_name) / item.relative_to(template_dir), exist_ok=True)

    # Replace the placeholder with the actual project name in all text files
    for file in Path(project_name).rglob('*'):
        if file.is_file():
            if file.suffix == '.py' and file.name != '__init__.py':
                try:
                    # Open file with utf-8 encoding
                    with file.open('r', encoding='utf-8') as f:
                        content = f.read()
                    content = content.replace(placeholder, project_name)
                    with file.open('w', encoding='utf-8') as f:
                        f.write(content)
                except UnicodeDecodeError:
                    print(f"Could not read file {file}. It might contain non-UTF-8 characters or binary data.")
                except Exception as e:
                    print(f"An error occurred while processing file {file}: {e}")

    print(f"Django project '{project_name}' has been created with custom template: brady template.")

if __name__ == "__main__":
    create_django_project()
