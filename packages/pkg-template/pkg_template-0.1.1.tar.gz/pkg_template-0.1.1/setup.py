from setuptools import setup, find_packages

setup(
    name="pkg_template",
    version="0.1.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pkg-template = pkg_template.cli:main',  # This connects the `pkg_template` command to the `main` function in `cli.py`.
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
