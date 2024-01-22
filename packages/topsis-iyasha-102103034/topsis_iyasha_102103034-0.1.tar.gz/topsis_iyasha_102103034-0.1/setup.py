from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
  long_description=long_description,
  long_description_content_type='text/markdown',
  name = 'topsis_iyasha_102103034',        # How you named your package folder (MyLib)
  packages = ['topsis_iyasha_102103034'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Topsis Package',   # Give a short description about your library
  author = 'iyasha',                   # Type in your name
  author_email = 'iiyasha_be21@thapar.edu',      # Type in your E-Mail
  keywords = ['TOPSIS', 'MCDM'],   # Keywords that define your package best
  install_requires=[            
          'numpy',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
  entry_points={
    'console_scripts': [
      'topsis=topsis_iyasha_102103034.topsis:main',
    ],
  },
)