from distutils.core import setup
setup(
  name = 'topsis-himanshu-102153030',         # How you named your package folder (MyLib)
  packages = ['topsis'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make      # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'self made library for topsis',   # Give a short description about your library
  author = 'Himanshu Mahlawat',                   # Type in your name
  author_email = 'himahlawat7@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  keywords = ['TOPSIS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
          'scipy.stats'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  include_package_data=True,
  entry_points={
      'console_scripts': [
            'topsis = topsis:102153030.py',
        ]
  }
  
)