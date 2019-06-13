# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from collective.campaingmonitor import _

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

    client_id = schema.Tuple(
        title=_(u"Client Id"),
        description=_(u"Client ids are used in Campaign Monitor to manage accounts, invoices, etc.", default=u""),
        value_type=schema.Choice(
            vocabulary="collective.campaignmonitor.CampaignMonitorClientsVocabulary"
        ),
        required=True,
    )



class ICampaignMonitorConnection(Interface):
    def initialize():
        """ Load connection data from registy and prepare for serving results """

    def lists():
        """ Return available lists at the campaign monitor account """
