from setuptools import setup, find_packages
import pkg_resources
import codecs
import os
#python setup.py sdist bdist_wheel

here = os.path.abspath(os.path.dirname(__file__))

with open('LICENSE.txt') as f:
    license = f.read()
with open('README.md') as f:
    readme = f.read()
VERSION = '0.0.1'
DESCRIPTION = 'Algorithm that allows neural network to grow while training'


# Setting up
setup(
    name="growingnn",
    version=VERSION,
    author="Szymon Świderski",
    author_email="<pjuralszymqn@gmail.com>",
    description=DESCRIPTION,
    license=license,
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_reqs = pkg_resources.parse_requirements('requirements.txt'),
    keywords=['python', 'neural network', 'growing neural network', 'growing'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"])
