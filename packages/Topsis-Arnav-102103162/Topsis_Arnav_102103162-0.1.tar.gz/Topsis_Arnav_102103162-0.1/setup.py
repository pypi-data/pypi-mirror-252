from distutils.core import setup
setup(
  name = 'Topsis_Arnav_102103162',         # How you named your package folder (MyLib)
  packages = ['Topsis_Arnav_102103162'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Contains the Topsis package by Arnav Sharma(102103162)',   # Give a short description about your library
  author = 'Arnav Sharma',                   # Type in your name
  author_email = 'arnavroh45@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/arnavroh45/Topsis_Arnav_102103162',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/arnavroh45/Topsis_Arnav_102103162/archive/refs/tags/0.1.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
      ],
)