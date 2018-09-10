from setuptools import setup, find_packages
import os

version = '1.0.0'

entry_points = {
    'openprocurement.auctions.core.plugins': [
        'auctions.tessel = openprocurement.auctions.tessel.includeme:includeme'
    ],
    'openprocurement.api.migrations': [
        'auctions.tessel = openprocurement.auctions.tessel.migration:migrate_data'
    ],
    'openprocurement.tests': [
        'auctions.tessel = openprocurement.auctions.tessel.tests.main:suite'
    ]
}

requires = [
    'setuptools',
    'openprocurement.auctions.core',
    'openprocurement.auctions.flash',
    'openprocurement.auctions.dgf',
]

docs_requires = requires + [
    'sphinxcontrib-httpdomain',
]
test_requires = requires + []

setup(name='openprocurement.auctions.tessel',
      version=version,
      description="",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Quintagroup, Ltd.',
      author_email='info@quintagroup.com',
      license='Apache License 2.0',
      url='https://github.com/openprocurement/openprocurement.auctions.tessel',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['openprocurement', 'openprocurement.auctions'],
      include_package_data=True,
      zip_safe=False,
      extras_require={'docs': docs_requires, 'test': test_requires},
      install_requires=requires,
      test_require=test_requires,
      entry_points=entry_points,
      )
