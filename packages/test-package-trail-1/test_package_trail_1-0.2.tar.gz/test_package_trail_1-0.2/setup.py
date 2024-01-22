from setuptools import setup, find_packages
setup(
   name='test_package_trail_1',
   version='0.2',
   packages=find_packages(),
   install_requires=[
      'click',
   ],
   entry_points='''
      [console_scripts]
      my_app=test_package_trail_1.my_app:hello
      ''',
)