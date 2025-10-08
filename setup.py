"""Installer for the collective.campaignmonitor package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="collective.campaignmonitor",
    version="2.0.1.dev0",
    description="CampaignMonitor integration for Plone",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Development Status :: 5 - Production/Stable",
    ],
    keywords="Python Plone",
    author="Mikel Larreategi",
    author_email="mlarreategi@codesyntax.com",
    url="https://github.com/collective/collective.campaignmonitor",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/collective.campaignmonitor",
        "Source": "https://github.com/collective/collective.campaignmonitor",
        "Tracker": "https://github.com/collective/collective.campaignmonitor/issues",
        # 'Documentation': 'https://collective.campaignmonitor.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.9",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "plone.api>=1.8.4",
        "createsend>=8.0.0",
        "Products.CMFPlone",
        "Zope",
        "z3c.form",
        "plone.app.registry",
        "plone.app.upgrade",
        "Products.GenericSetup",
        "plone.protect",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
            "plone.base",
            "plone.browserlayer",
            "zope.schema",
            "zope.component",
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.campaignmonitor.locales.update:update_locale
    """,
)
