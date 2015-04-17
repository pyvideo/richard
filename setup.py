# richard -- video index system
# Copyright (C) 2012, 2013, 2014, 2015 richard contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

requirements = [
    'bleach==1.4.1',
    'django==1.7.7',
    'djangorestframework==2.3.14',
    'django-browserid==0.11.1',
    'django-configurations==0.8',
    'django-grappelli==2.5.2',
    'django-haystack==2.3.1',
    'dj-database-url==0.3.0',
    'fancy_tag==0.2.0',
    'Markdown==2.6.1',
    'requests==2.6.0',
    'pytz==2014.10',
    'whoosh==2.5.7',
]

development_requirements = [
    'factory_boy==2.4.1',
    'httmock==1.2.3',
    'mock==1.0.1',
    'pytest-django==2.8.0',
    'Pygments==2.0.1',
    'Sphinx==1.3.1',
    'steve==0.4',
    'tox==1.9.2',
    'eadred==0.3',
    'pre-commit==0.4.4',
]

postgre_requirements = [
    'psycopg2==2.6',
]


setup(name='richard',
      version='0.1.0',
      description='Video indexing site',
      author='Will Kahn-Greene',
      author_email='',
      license='AGPLv3',
      install_requires=requirements,
      extras_require={
          'dev': development_requirements,
          'postgresql': postgre_requirements,
      },
      packages=find_packages('src'),
      package_dir={'': 'src'},
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
      ]
)
