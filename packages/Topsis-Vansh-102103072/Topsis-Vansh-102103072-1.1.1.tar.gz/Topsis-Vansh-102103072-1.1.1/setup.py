import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
  name = 'Topsis-Vansh-102103072',          
  packages = ['topsis'],  
  version = '1.1.1',     
  license='MIT',    
  description = 'This is a library for implementing Topsis in command line',
  long_description=README,
  long_description_content_type="text/markdown",  
  author = 'Vansh Batra',                   
  author_email = 'batravansh162@gmail.com',      
  url = 'https://github.com/Vansh-Batra10/Topsis-Vansh-102103072',   
  download_url = 'https://github.com/Vansh-Batra10/Topsis-Vansh-102103072/archive/refs/tags/v1.1.1.tar.gz ',    
  keywords = ['TOPSIS', 'Command Line'],   
  install_requires=[            
          'numpy',
          'pandas'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
  ],
  entry_points={
        "console_scripts": [
            "topsis=topsis.__main__:main",
        ]
    },
)
