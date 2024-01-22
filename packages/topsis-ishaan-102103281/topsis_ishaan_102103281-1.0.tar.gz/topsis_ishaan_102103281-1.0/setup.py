import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
  long_description=README,
  long_description_content_type='text/markdown',
  name = 'topsis_ishaan_102103281',       
  version = '1.0',     
  license='MIT',      
  description = 'TOPSIS',
  author = 'Ishaan Gaba',
  author_email = 'igaba_be21@thapar.edu',      
  keywords = ['TOPSIS', 'MCDM'],   
  install_requires=[            
          'numpy',
          'pandas',
        ],
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
  ],
  entry_points={
    'console_scripts': [
      'topsis=topsis_ishaan_102103281.main:main',
    ],
  },
)