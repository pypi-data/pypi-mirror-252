from setuptools import setup, find_packages
setup(
   name='test_package_trail_1',
   version='0.1',
   packages=find_packages(),
   install_requires=[
      'click',
   ],
   entry_points='''
      [console_scripts]
      my_cli_app=test_package_trail_1.my_app:hello
      ''',
)