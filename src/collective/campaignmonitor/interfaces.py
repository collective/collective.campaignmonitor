# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.campaignmonitor import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


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


class ICampaignMonitorConnection(Interface):
    def initialize():
        """ Load connection data from registy and prepare for serving results """

    def account():
        """ Return account information from campaign monitor """

    def clients():
        """ Return available clients at the campaign monitor account """

    def lists():
        """ Return available lists at the campaign monitor account """
