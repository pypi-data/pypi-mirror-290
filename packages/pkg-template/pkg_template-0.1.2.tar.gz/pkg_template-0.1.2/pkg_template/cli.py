import argparse
import os
import re
import logging

def create_template(template_name):
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

def main():
    parser = argparse.ArgumentParser(description="Create a PyPI package template or update the version.")
    
    # Add arguments
    parser.add_argument("-c", "--create-template", type=str, help="Create the template with name.")
    parser.add_argument("-u", "--update-version", type=str, help="Update your package version.")
    parser.add_argument("-v", "--version", action="version", version="pkg_template 0.1.2")
    parser.add_argument("-f", "--force", action="store_true", help="Use with --update-version to skip confirmation prompt.")
    parser.add_argument("-p", "--path", type=str, default=os.getcwd(), help="Path to the setup.py file (default is current directory).")
    
    args = parser.parse_args()

    if args.create_template:
        create_template(args.create_template)
    
    elif args.update_version:
        setup_path = os.path.join(args.path, 'setup.py')
        if not args.force:
            sure_ = input(f"Are you sure you want to update the version in {setup_path}? [Y:yes, N:no]: ")
            if sure_.lower() != 'y':
                return
        
        update_version(args.update_version, setup_path)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
