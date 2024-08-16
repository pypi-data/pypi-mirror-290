from setuptools import setup, find_packages

setup(
    name="pkg_template",
    version="0.1.3",
    packages=find_packages(),
    package_data={
        'pkg_template': ['data/django_app/**/*', "data/*"],
    },
    include_package_data=True,  # Make sure this is included
    entry_points={
        'console_scripts': [
            'pkg-template = pkg_template.cli:main',
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
