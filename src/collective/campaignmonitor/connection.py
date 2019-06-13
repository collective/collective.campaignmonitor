from collective.campaignmonitor.interfaces import ICampaignMonitorConnection
from collective.campaignmonitor.interfaces import ICampaignMonitorSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtilty
from zope.interface import implementer
from createsend import *

from logging import getLogger

log = getLogger("CampaignMonitorConnection")


@implementer(ICampaignMonitorConnection)
class CampaingMonitorConnection(object):
    def __init__(self):
        self.registry = None
        self.settings = None

    def initialize(self):
        if self.registry is None:
            self.registry = getUtility(IRegistry)
        if self.settings is None:
            self.settings = self.registry.forInterface(ICampaignMonitorSettings)

        self.api_key = self.settings.api_key

    def clients(self):
        self.initialize()
        cs = CreateSend({"api_key": self.api_key})
        results = []
        try:
            clients = cs.clients()
            for client in clients:
                data = dict(client_id=client.ClientID, client_name=client.Name)
                results.append(data)
        except createsend.Unauthorized as e:
            log.info(str(e))

        return results

    def lists(self):
        self.initialize()
        cs = Client({"api_key": self.api_key}, self.settings.client_id)
        results = []
        try:
            lists = cs.lists()

            for listitem in lists:
                data = dict(list_id=listitem.ListID, list_name=listitem.Name)
                results.append(data)
        except createsend.Unauthorized as e:
            log.info(str(e))

        return results
