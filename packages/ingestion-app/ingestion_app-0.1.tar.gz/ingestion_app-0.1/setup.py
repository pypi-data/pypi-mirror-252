from setuptools import setup, find_packages
setup(
   name='ingestion_app',
   version='0.1',
   packages=find_packages(),
   install_requires=[
      'click',
   ],
   entry_points='''
      [console_scripts]
      my_cli_app=ingestion_app.my_cli_app:hello
      ''',
)