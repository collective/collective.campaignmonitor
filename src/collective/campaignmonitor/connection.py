from collective.campaignmonitor.interfaces import ICampaignMonitorConnection
from collective.campaignmonitor.interfaces import ICampaignMonitorSettings
from createsend import Client
from createsend import CreateSend
from logging import getLogger
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implementer


log = getLogger("CampaignMonitorConnection")


CLIENTS_CACHE_KEY = "collective.campaignmonitor.cache.clients"
LISTS_CACHE_KEY = "collective.campaignmonitor.cache.lists"


_marker = None


@implementer(ICampaignMonitorConnection)
class CampaignMonitorConnection(object):
    def __init__(self):
        self.registry = None
        self.settings = None

    def initialize(self):
        if self.registry is None:
            self.registry = getUtility(IRegistry)
        if self.settings is None:
            self.settings = self.registry.forInterface(ICampaignMonitorSettings)

        self.api_key = self.settings.api_key

    def update_cache(self):

        self.initialize()
        if not self.settings.api_key:
            return

        clients = self._clients()
        if type(clients) is list:
            clients = tuple(clients)
            if self.registry[CLIENTS_CACHE_KEY] != clients:
                self.registry[CLIENTS_CACHE_KEY] = clients

        lists = self._lists()
        if type(lists) is list:
            lists = tuple(lists)
            if self.registry[LISTS_CACHE_KEY] != lists:
                self.registry[LISTS_CACHE_KEY] = lists

    def _clients(self):
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

    def clients(self):
        self.initialize()
        cache = self.registry.get(CLIENTS_CACHE_KEY, _marker)
        if cache and cache is not _marker:
            return cache
        return self._clients()

    def _lists(self):
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

    def lists(self):
        self.initialize()
        cache = self.registry.get(LISTS_CACHE_KEY, _marker)
        if cache and cache is not _marker:
            return cache
        return self._lists()
