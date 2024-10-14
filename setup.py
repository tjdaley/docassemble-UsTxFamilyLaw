import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')

VERSION = '1.0.4'

def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.UsTxFamilyLaw',
      version=VERSION,
      description=('Texas Family Law Forms'),
      long_description='# US-TX-Family_Law\r\n## Docassemble Package for Family Law forms in Texas, United States\r\n### Author: Thomas J. Daley, J.D.\r\n\r\n# Available Interviews\r\n\r\n## Inventory & Appraisement\r\n\r\n## Notice to Vacate\r\n\r\n## Promissory Note for Loan for Legal Fees\r\n\r\n## Roommate Early Move Out Incentive Agreement\r\n',
      long_description_content_type='text/markdown',
      author='Thomas J. Daley, J.D.',
      author_email='tom@powerdaley.com',
      license='The MIT License',
      url='https://da.jdbot.us',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=[],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/UsTxFamilyLaw/', package='docassemble.UsTxFamilyLaw'),
     )

