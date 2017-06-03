from setuptools import setup, find_packages

README = 'use python2 modules in python3'

requires = [ 'flask',
             'requests', ]
tests_require = [
        'pytest',
        ]

setup(name='warp2',
      version='0.0.1',
      description=README,
      long_description=README,
      url='https://github.com/haarcuba/warp2',
      classifiers=[
          "Programming Language :: Python",
      ],
      author='Yoav Kleinberger',
      author_email='haarcuba@gmail.com',
      keywords='subprocess',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      )
