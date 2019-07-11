.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==========================
collective.campaignmonitor
==========================

.. image:: https://travis-ci.com/collective/collective.campaignmonitor.svg?branch=master
    :target: https://travis-ci.com/collective/collective.campaignmonitor

.. image:: https://coveralls.io/repos/github/collective/collective.campaignmonitor/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.campaignmonitor?branch=master


Campaign Monitor integration in Plone.

Heavily based on `collective.mailchimp`_ by `Timo Stollenwerk`_

Like `collective.mailchimp`_ this product provides a portlet and a view (@@cm-newsletter-subscribe) to let users subscribe to a newsletter.

The product provides a configuration control panel to let sites admins enter the Campaing Monitor API Key and select a customer, this way the available list of this customer will be selectable both in the subscribe form and in the portlet.

This product has been tested on Plone 5.1 and above.


Installation
------------

Install collective.campaignmonitor by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.campaignmonitor


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.campaignmonitor/issues
- Source Code: https://github.com/collective/collective.campaignmonitor


Support
-------

If you are having issues, please let us know using GitHub issues.


License
-------

The project is licensed under the GPLv2.


.. _`Timo Stollenwerk`: http://github.com/tisto
.. _`collective.mailchimp`: https://pypi.org/project/collective.mailchimp
