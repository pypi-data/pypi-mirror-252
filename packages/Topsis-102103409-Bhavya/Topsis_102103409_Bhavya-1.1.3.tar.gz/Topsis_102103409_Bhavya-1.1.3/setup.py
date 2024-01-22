from setuptools import setup
setup(
  name = 'Topsis_102103409_Bhavya',         
  packages = ['Topsis_102103409_Bhavya'],   
  version = '1.1.3',      
  license='MIT',       
  description = 'This package helps to get the topsis score from the given dataframe',   # Give a short description about your library
  author = 'Bhavya Rampal',                   # Type in your name
  author_email = 'bhavya3728@gmail.com',      # Type in your E-Mail
  keywords = ['Topsis', 'Ranking'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
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
  ],
)
