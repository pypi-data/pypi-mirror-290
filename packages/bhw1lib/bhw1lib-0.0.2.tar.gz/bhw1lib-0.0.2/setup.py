from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='bhw1lib',
  version='0.0.2',
  author='Timur Ratnikov',
  author_email='timur2640rt@gmail.com',
  description='',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='',
  packages=find_packages(),
  install_requires=[''],
  classifiers=[],
  keywords='',
  project_urls={},
  python_requires='>=3.9'
)
