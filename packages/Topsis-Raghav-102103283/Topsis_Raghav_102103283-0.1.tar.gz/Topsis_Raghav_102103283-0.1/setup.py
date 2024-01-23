from distutils.core import setup
setup(
  name = 'Topsis_Raghav_102103283',
  version = '0.1',
  license='MIT',        
  description = 'Topsis package python',
  author = 'Raghav Garg',                   
  author_email = 'rgarg5_be21@thapar.edu',
  keywords = ['Python', 'Topsis', 'UCS633'],   
  install_requires=[ 
          'validators',
          'beautifulsoup4',
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