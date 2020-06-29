# -*- coding: utf-8 -*-
from collective.campaignmonitor import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

import re


class ICollectiveCampaignmonitorLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICampaignMonitorSettings(Interface):
    api_key = schema.TextLine(
        title=_(u"CampaignMonitor API Key"),
        description=_(
            u"help_api_key",
            default=u"Enter in your CampaignMonitor key here (.e.g. "
            + u"'8b785dcabe4b5aa24ef84201ea7dcded-us4'). Log into "
            + u"xxxx.createsend.com, go to account settings -> API Keys "
            + u"click on Show API key and copy the API Key to this field.",
        ),
        default=u"",
        required=True,
    )

    client_id = schema.Choice(
        title=_("Client ID"),
        description=_(
            u"Campaign Monitor uses clients to group lists, invoices, ... Select the one that you want to use in Plone"
        ),
        vocabulary="collective.campaignmonitor.CampaignMonitorClientsVocabulary",
        required=False,
    )

    force_resubscribe = schema.Bool(
        title=_("Force resubscription in default form?"),
        description=_(
            u"When adding a new subscriber from the API, Campaign Monitor checks if the user was previously unsubscribed from the list and if so it prevents from adding it. If this option is enabled, this check is bypassed. Be careful when using this option."
        ),
        default=False,
    )


class ICampaignMonitorConnection(Interface):
    def initialize():
        """ Load connection data from registy and prepare for serving results """

    def account():
        """ Return account information for campaign monitor """

    def clients():
        """ Return available clients at the campaign monitor account """

    def lists():
        """ Return available lists at the campaign monitor account """

    def subscribe(email, list_id):
        """ Subscribe 'email' to 'list_id' Campaign Monitor list """

    def list_details(list_id):
        """ get details about a given list """


class NotAnEmailAddress(schema.ValidationError):
    __doc__ = _(u"Invalid email address")


check_email = re.compile(r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+.)*[a-zA-Z]{2,4}").match


def validate_email(value):
    if not check_email(value):
        raise NotAnEmailAddress(value)
    return True


class INewsletterSubscribe(Interface):

    email = schema.TextLine(
        title=_(u"Email address"),
        description=_(u"help_email", default=u"Please enter your email address."),
        required=True,
        constraint=validate_email,
    )

    list_id = schema.Choice(
        title=_(u"List ID"),
        vocabulary="collective.campaignmonitor.CampaignMonitorListsVocabulary",
        required=False,
    )
