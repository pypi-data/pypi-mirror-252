from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '1.1.0'
DESCRIPTION = 'nah you just started'

# Setting up
setup(
    name="subhangpack",
    version=VERSION,
    author="SubhangMokkarala",
    author_email="subhangmokkarala@gmail.com",
    description=DESCRIPTION,
    long_description= open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['numpy'],
    entry_points={
        'console_scripts': [
            'subhangpack-hello = subhangpack:hello',
            'subhangpack-devicename = subhangpack:namegen',
            'subhangpack-info = subhangpack:sysinfo'
        ]
    },
    keywords=['python', 'name','beginner', 'generator', 'device', 'random', 'fun', 'subhangpack', 'subhang', 'mokkarala', 'subhangmokkarala'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
