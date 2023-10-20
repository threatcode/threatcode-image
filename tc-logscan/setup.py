import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

with open(f'{HERE}/README.md') as f:
  readme = f.read()

with open(f'{HERE}/requirements.txt') as f:
  required = f.read().splitlines()

with open(f'{HERE}/requirements-dev.txt') as f:
  dev_required = f.read().splitlines()
  dev_required = dev_required[1:]

setup(
  name='logscan',
  version='0.0.1',
  description='Threat Code ML Log Scanning and Prediction',
  long_description=readme,
  long_description_content_type='text/markdown',
  author='Sagar Singhal, William Wernert',
  url='https://github.com/threatcode/threatcode-image/tree/master/tc-logscan',
  packages=find_packages(where='src'),
  package_dir={'':'src'},
  include_package_data=True,
  install_requires=required,
  extras_require={
    'dev': dev_required,
  },
  entry_points= {
    'console_scripts': [
      'tc-logscan=logscan.run:main'
    ]
  }
)
