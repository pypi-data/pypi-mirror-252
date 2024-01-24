from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.6'
DESCRIPTION = 'A libirary to automate developing keras models'
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# Setting up
setup(
    name="dl-assistant",
    version=VERSION,
    author="Ayush Agrawal",
    author_email="aagrawal963@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['tensorflow','keras','notebook','tqdm','scikit-learn'],
    keywords=[
        'Automated Deep Learning',
        'Model Generation',
        'Neural Network Automation',
        'Deep Learning Automation',
        'AI Model Builder',
        'Neural Architecture Search (NAS)',
        'Automated Model Design',
        'Deep Learning Toolkit',
        'Effortless Model Creation',
        'Model Composer',
        'AI Model Automation',
        'Neurogeneration',
        'DL Model Composer',
        'Smart Model Builder',
        'AI Model Generator',
        'Ayush Agrawal',
        'tensorflow',
        'keras'
],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)