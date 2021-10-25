# -*- coding: utf-8 -*-
"""Installer for the collective.campaignmonitor package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join(
    [
        open('README.rst').read(),
        open('CONTRIBUTORS.rst').read(),
        open('CHANGES.rst').read(),
    ]
)


setup(
    name='collective.campaignmonitor',
    version='1.3',
    description="CampaingMonitor integration for Plone",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Mikel Larreategi',
    author_email='mlarreategi@codesyntax.com',
    url='https://github.com/collective/collective.campaignmonitor',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/collective.campaignmonitor',
        'Source': 'https://github.com/collective/collective.campaignmonitor',
        'Tracker': 'https://github.com/collective/collective.campaignmonitor/issues',
        # 'Documentation': 'https://collective.campaignmonitor.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'plone.api>=1.8.4',
        'createsend>=6.0.0,<7.0.0',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.campaignmonitor.locales.update:update_locale
    """,
)
