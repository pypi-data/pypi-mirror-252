import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
  long_description=README,
  long_description_content_type='text/markdown',
  name = 'topsis-yogesh-102103022',       
  version = '1.0',     
  license='MIT',      
  description = 'TOPSIS',
  author = 'YogeshRathee',
  author_email = 'yrathee_be21@thapar.edu',      
  keywords = ['TOPSIS'],   
  install_requires=[            
          'numpy',
          'pandas',
        ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
  ],
  entry_points={
    'console_scripts': [
      'topsis=topsis_yogesh_102103022.main:main',
    ],
  },
)