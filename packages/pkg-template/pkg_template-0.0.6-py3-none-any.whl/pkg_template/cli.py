import argparse, os

def main():    
    parser = argparse.ArgumentParser(description="create a pypi pkg template")
    
    #add arguments
    parser.add_argument("-c", "--create-template", type=str, help="create the template with name")
    parser.add_argument("-v", "--version", action="version", version="pkg_template 0.0.3")
    
    args = parser.parse_args()


    if args.create_template:
        final_directory = f"{os.getcwd()}/{args.create_template}"
        if not os.path.exists(final_directory):
            print(final_directory)
            
            os.makedirs(final_directory)
            os.makedirs(f"{final_directory}/{args.create_template}")
        
        
        
        the_setup = """from setuptools import setup, find_packages
    
setup(
name="pkg_template",
version="0.0.1",
packages=find_packages(),
entry_points={
    'console_scripts': [ #if you want to your package connect to cmd or command prompt
        'pkg_template = pkg_template.cli:main',  # This connects the `pkg_template` command to the `main` function in `cli.py`.
    ],
},
install_requires=[
    # 'requests',
],
author="amirgard",
author_email="",
description="",
long_description=open('README.md').read(),
long_description_content_type='text/markdown',
url="",
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
python_requires='>=3.6',
)
"""
        
        with open(f"{final_directory}/setup.py", "w") as f:
                f.write((the_setup.replace("pkg_template", args.create_template)))
        with open(f"{final_directory}/README.md", "w") as f:
            f.write(" ")
        with open(f"{final_directory}/{args.create_template}/__init__.py", "w") as f:
            f.write(" ")
        with open(f"{final_directory}/{args.create_template}/cli.py", "w") as f:
            f.write(" ")
    else:
        print("options: \n-c, -create-template <name of your template> -> create the template\n-v, --version -> show the version of this pakage")
if __name__ == "__main__":
    main()