from setuptools import setup, find_packages
import codecs
import os


VERSION = '1'
DESCRIPTION = "This is going to be game changer as there is no such project in this world we are going to make hardware soon for it and it's second version going to be boom"
LONG_DESCRIPTION = """

 ___                       _    _  _                       
/ __> _ _  _ _  _ _  ___  | |  <_>| |_  _ _  ___  _ _  _ _ 
\__ \| | || '_>| | |<_> | | |_ | || . \| '_><_> || '_>| | |
<___/`___||_|  `_. |<___| |___||_||___/|_|  <___||_|  `_. |
               <___'                                  <___'

This project uses Python to develop a virtual library application that can generate and display comprehensive courses and books on any given topic. The application employs AI for content creation and includes the following key features:

Content Generation: Utilizes AI models to create detailed courses and books, covering various topics.
PDF Creation: Converts generated content into structured PDF documents.
GUI with PyQt5: Features an aesthetically pleasing, black-themed user interface for topic input, content generation, and PDF viewing.
Interactive PDF Viewer: Displays generated PDFs within the application for easy access and reading.
This project aims to provide a user-friendly tool for generating educational material efficiently.
"""

# Setting up
setup(
    name="Surya_Course_generator",
    version=VERSION,
    author="Suraj sharma",
    author_email="Surajsharma963472@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        'qtwidgets',
        'PyMuPDF',
        'webscout',
        'fpdf',
        'rich'
    ],
    keywords=['Surya', 'Game changer', 'GUI', 'python tutorial', 'Suraj', 'Dictionary', 'Library', 'LLAMA', 'AI'],
)