from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'Mass mail sender with custom tweaks'

with open('README.md') as f:
    long = f.read()
setup(
        name="mailez", 
        version=VERSION,
        author="Mehmet Utku OZTURK",
        author_email="<contact@ælphard.tk>",
        description=DESCRIPTION,
        long_description=long,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=["pandas"],
        
        keywords=['email', 'mail'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "Programming Language :: Python :: 3"
        ]
)