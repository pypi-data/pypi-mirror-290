import os
from setuptools import setup, find_packages

script_directory = os.path.abspath(os.path.dirname(__file__))

package_name = "rule_evaluator"
version = None
with open(os.path.join(script_directory, package_name, '__init__.py')) as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith("__version__"):
            version = line.split("=")[-1].strip().strip('"')
assert version is not None, f"Check version in {package_name}/__init__.py"

with open(os.path.join(script_directory, 'README.md')) as f:
    long_description = f.read()

# Requirements
requirements = list()
with open(os.path.join(script_directory, 'requirements.txt')) as f:
    for line in f.readlines():
        line = line.strip()
        if line:
            if not line.startswith("#"):
                requirements.append(line)

setup(
    name=package_name,
    python_requires='>=3.7',
    version=version,
    description='Lightweight Python-based nested rule evaluator',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Specify Markdown


    # The project's main homepage.
    url='https://github.com/jolespin/rule_evaluator',

    # Author details
    author='Josh L. Espinoza',

    # Choose your license
    license='GPLv3',
    packages=find_packages(),
    
    install_requires=requirements, #[:-1],
    tests_require=requirements, #[-1:]
)