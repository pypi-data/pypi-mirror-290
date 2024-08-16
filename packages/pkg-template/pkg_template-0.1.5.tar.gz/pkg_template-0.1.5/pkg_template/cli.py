import argparse
import os
import re
import logging
import subprocess
import shutil
import pkg_resources

def pip_create_template(template_name):
    """Creates a basic PyPI package template with the specified name."""
    final_directory = os.path.join(os.getcwd(), template_name)
    package_dir = os.path.join(final_directory, template_name)
    data_dir = os.path.join(package_dir, 'data')
    
    # Create directories
    os.makedirs(data_dir, exist_ok=True)
    
    # Write setup.py
    setup_content = f"""from setuptools import setup, find_packages
setup(
    name="{template_name}",
    version="0.0.1",
    packages=find_packages(),
    package_data={{
        '{template_name}': ['data/*'],  # Include all files in the 'data' directory
    }},
    entry_points={{
        'console_scripts': [
            '{template_name} = {template_name}.cli:main',
        ],
    }},
    install_requires=[
        # 'requests',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A description of your package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/yourproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
"""
    create_file(os.path.join(final_directory, 'setup.py'), setup_content)
    create_file(os.path.join(final_directory, 'README.md'), "# Project Title")
    create_file(os.path.join(package_dir, '__init__.py'), "")
    create_file(os.path.join(package_dir, 'cli.py'), "def main():\n    print('Hello from the CLI!')")
    
    # Optional: Create additional common files
    create_file(os.path.join(final_directory, '.gitignore'), "*.pyc\n__pycache__/")
    create_file(os.path.join(final_directory, 'LICENSE'), "MIT License")
    create_file(os.path.join(final_directory, 'requirements.txt'), "")

    logging.info(f"Template created at {final_directory}")

def create_file(path, content):
    """Helper function to create a file with the given content."""
    with open(path, 'w') as f:
        f.write(content)
    logging.info(f"Created {path}")

def update_version(version, setup_path):
    """Updates the version in the specified setup.py file."""
    if not os.path.exists(setup_path):
        logging.error(f"setup.py not found at {setup_path}")
        return
    
    with open(setup_path, 'r+') as f:
        file_text = f.read()
        version_pattern = re.compile(r'version\s*=\s*[\'"]([^\'"]+)[\'"]')
        match = version_pattern.search(file_text)
        
        if match:
            current_version = match.group(1)
            file_text = file_text.replace(current_version, version)
            f.seek(0)
            f.write(file_text)
            f.truncate()
            logging.info(f"Version updated from {current_version} to {version} in {setup_path}")
        else:
            logging.error("Version string not found in setup.py.")

def django_create_template(template_name: str):
    """Crate a django template using django"""
    
    # Step 1: Create the Django project
    subprocess.run(["django-admin", "startproject", template_name], check=True)
    subprocess.run(f"cd {template_name}")
    
    # Step 2: Change the working directory to the project directory
    # project_path = os.path.join(os.getcwd(), template_name)
    os.chdir(os.getcwd())
    with open(os.path.join(os.getcwd(), template_name, "urls.py"), "r+") as f:
        file_text = f.read()
        
        f.seek(0)
        f.write()
        f.truncate()
def create_app(app_name: str, project_path=os.getcwd()):
    main_path = os.path.join(project_path, app_name)
    os.makedirs(main_path, exist_ok=True)
    
    data_path = pkg_resources.resource_filename('pkg_template', 'data/django_app')
    
    if os.path.exists(data_path):
        for item in os.listdir(data_path):
            s = os.path.join(data_path, item)
            d = os.path.join(main_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)  # Python 3.8+ allows dirs_exist_ok
            else:
                shutil.copy2(s, d)
                        
        settings_path = os.path.join(project_path, project_path.split("\\")[-1], "settings.py")
        urls_path = os.path.join(project_path, project_path.split("\\")[-1], "urls.py")
        app_app_path = os.path.join(project_path, app_name, "apps.py")
        
        # config the app class in apps.py
        with open(app_app_path, "r+") as f:
            file_text = f.read()
            file_text = file_text.replace("MainConfig", f"{get_classed_name(app_name)}Config")
            file_text = file_text.replace("main", f"{app_name}")
            
            f.seek(0)
            f.write(file_text)
            f.truncate()
        # config the app in settings.py
        with open(settings_path, "r+") as f:
            # Read the entire file content
            file_text = f.read()
            
            # Find the position of the INSTALLED_APPS list
            start_index = file_text.find("INSTALLED_APPS = [") + len("INSTALLED_APPS = [")
            end_index = file_text.find("]", start_index)
            
            # Extract the current list of installed apps
            installed_apps = file_text[start_index:end_index].strip()
            
            # Convert the installed apps to a list
            app_list = installed_apps.split(",")
            
            # Clean up app_list by removing any empty strings
            app_list = [app.strip() for app in app_list if app.strip()]
            
            if app_list[-1] == "":
                app_list.pop()

            # Add the new app name
            app_list.append(f"'{app_name}.apps.{get_classed_name(app_name)}Config'")

            new_installed_apps = ",\n    ".join(app_list)+","
            
            # Replace the old INSTALLED_APPS list with the new one
            file_text = file_text[:start_index] + "\n    " + new_installed_apps + "\n" + file_text[end_index:]
            
            # Write the updated content back to the file
            f.seek(0)
            f.write(file_text)
            f.truncate() 
        # config the app in urls.py
        with open(urls_path, "r+") as f:
            file_text = f.read()
            start_index = file_text.rfind(",\n") +1
            file_text = file_text[0:start_index] + f"\n    path('', include('{app_name}.urls'))," + file_text[start_index::]
            # Write the updated content back to the file
            f.seek(0)
            f.write(file_text)
            f.truncate()
    else:
        print(f"The directory {data_path} does not exist.")

def get_classed_name(string: str):
    result = f"{string[0:1].upper()}{string[1::]}"
    
    while (finded:=result.find("_")) != -1:
        result = result.replace("_", "", 1)
        result = result[0:finded] + get_classed_name(result[finded::])
        
    return result

def main():
    parser = argparse.ArgumentParser(description="Create a PyPI package template or update the version.")
    
    # Add arguments
    parser.add_argument("-c", "--create-template", type=str, help="Create the template with name.")
    parser.add_argument("-u", "--update-version", type=str, help="Update your package version.")
    parser.add_argument("-v", "--version", action="version", version="pkg_template 0.1.2")
    parser.add_argument("-f", "--force", action="store_true", help="Use with --update-version to skip confirmation prompt.")
    parser.add_argument("-p", "--path", type=str, default=os.getcwd(), help="Path to the setup.py file (default is current directory).")
    parser.add_argument("-d", "--create-django-project", type=str, help="Create the django template")
    parser.add_argument("-a", "--create-django-app", type=str, help="create a django app and config it")
    
    
    args = parser.parse_args()

    if args.create_template:
        pip_create_template(args.create_template)
    
    elif args.update_version:
        setup_path = os.path.join(args.path, 'setup.py')
        if not args.force:
            sure_ = input(f"Are you sure you want to update the version in {setup_path}? [Y:yes, N:no]: ")
            if sure_.lower() != 'y':
                return
        
        update_version(args.update_version, setup_path)
    
    elif args.create_django_project:
        django_create_template(args.create_django_project)
    
    elif args.create_django_app:
        create_app(app_name=args.create_django_app, project_path=args.path)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
