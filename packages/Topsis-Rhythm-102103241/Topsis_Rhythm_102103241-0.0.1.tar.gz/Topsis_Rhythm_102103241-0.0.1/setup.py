from setuptools import setup,find_packages
setup(
  name = 'Topsis_Rhythm_102103241',         # How you named your package folder (MyLib)
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'table generator',   # Give a short description about your library
  author = 'Rhythm',                   # Type in your name
  author_email = '',      # Type in your E-Mail
  url = '',   # Provide either the link to your github or to your website
  keywords = [''],   # Keywords that define your package best
  install_requires=[''],        
  packages=find_packages() ,
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    
  ],
)