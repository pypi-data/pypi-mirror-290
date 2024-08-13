from setuptools import setup, find_packages

setup(
   name='scarx_api_client',
   version='0.6.2',
   description='Client for Scarx API',
   long_description=open('README.md').read(),
   long_description_content_type='text/markdown',
   author='Scartz',
   author_email='github@scarx.net',
   packages=find_packages(),
   install_requires=['grpclib', 'betterproto==2.0.0b6', 'pydantic'],
)
