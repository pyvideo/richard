from setuptools import setup, find_packages

requirements = [
    'bleach==1.4',
    'django==1.6.5',
    'djangorestframework==2.3.10',
    'django-browserid==0.10.1',
    'django-configurations==0.8',
    'django-grappelli==2.5.2',
    'django-haystack==2.1.0',
    'dj-database-url==0.3.0',
    'eadred==0.3',
    'Markdown==2.3.1',
    'requests==2.1.0',
    'South==0.8.4',
    'whoosh==2.5.6',
]

development_requirements = [
    'factory_boy==2.4.1',
    'httmock==1.2.2',
    'pytest-django==2.6.2',
    'Pygments',
    'Sphinx',
    'steve',
    'tox==1.7.1',
]

postgre_requirements = [
    'psycopg2',
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
