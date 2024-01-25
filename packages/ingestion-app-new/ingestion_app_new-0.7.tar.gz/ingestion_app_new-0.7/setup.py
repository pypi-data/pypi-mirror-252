from setuptools import setup, find_packages
setup(
   name='ingestion_app_new',
   version='0.7',
   packages=find_packages(),
   install_requires=[
      'click',
   ],
   entry_points='''
      [console_scripts]
      my_cli_app=ingestion_app_new.my_cli_app:main
      ''',
)

