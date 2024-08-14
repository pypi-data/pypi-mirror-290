from setuptools import setup, find_packages
import codecs
import os


VERSION = '1'
DESCRIPTION = ("""

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
               
To use the module please write this code in python compiler

from Surya_Course_maker import Main
Main()
               
THNX and we are hereby sure u will be getting it's new version soon....

            
""")
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
    name="Surya_Course_maker",
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