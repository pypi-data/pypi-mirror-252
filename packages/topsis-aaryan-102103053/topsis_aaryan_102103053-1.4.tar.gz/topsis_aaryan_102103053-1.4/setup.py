from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
  long_description=long_description,
  long_description_content_type='text/markdown',
  name = 'topsis_aaryan_102103053',         # How you named your package folder (MyLib)
  packages = ['topsis_aaryan_102103053'],   # Chose the same as "name"
  version = '1.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Library for dealing with Multiple Criteria Decision Making (MCDM) problems by applying Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS).',   # Give a short description about your library
  author = 'Aaryan Gupta',                   # Type in your name
  author_email = 'aaryang991@gmail.com',      # Type in your E-Mail
  url = '',   # Provide either the link to your github or to your website
  download_url = '',    # I explain this later on
  keywords = ['TOPSIS', 'MCDM'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
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
            'topsis_aaryan_102103053=topsis_aaryan_102103053.__main__:main',
        ],
    },
)
