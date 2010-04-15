from distutils.core import setup

long_description = open('README.rst').read()

setup(name="python-yammer",
      version='0.2.0',
      py_modules=["yammer"],
      description="Library for interacting with the Yammer API",
      author="James Turk",
      author_email = "jturk@sunlightfoundation.com",
      license='BSD',
      url="http://github.com/sunlightlabs/python-yammer/",
      long_description=long_description,
      platforms=["any"],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
      )

