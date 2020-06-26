# -*- coding: utf-8 -*-
from collective.campaignmonitor.interfaces import ICampaignMonitorConnection
from collective.campaignmonitor.interfaces import ICampaignMonitorSettings
from createsend import BadRequest
from createsend import Client
from createsend import CreateSend
from createsend import List
from createsend import Subscriber
from createsend import Unauthorized
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
        self.api_key = None

    def initialize(self):
        if self.registry is None:
            self.registry = getUtility(IRegistry)
        if self.settings is None:
            self.settings = self.registry.forInterface(ICampaignMonitorSettings)

        self.api_key = self.settings.api_key

    def account(self):
        self.initialize()
        return self.api_key

    def update_cache(self):
        log.info("Updating cache...")
        self.initialize()
        if not self.settings.api_key:
            return

        clients = self._clients()
        if type(clients) is list:
            clients = tuple(clients)
            if self.registry[CLIENTS_CACHE_KEY] != clients:
                self.registry[CLIENTS_CACHE_KEY] = clients
                log.info("Updated client list.")

        lists = self._lists()
        if type(lists) is list:
            lists = tuple(lists)
            if self.registry[LISTS_CACHE_KEY] != lists:
                self.registry[LISTS_CACHE_KEY] = lists
                log.info("Update lists list")

        log.info("Updating cache finished.")

    def _clients(self):
        cs = CreateSend({"api_key": self.api_key})
        results = []
        try:
            clients = cs.clients()
            for client in clients:
                data = dict(client_id=client.ClientID, client_name=client.Name)
                results.append(data)
        except Unauthorized as e:
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
        except Unauthorized as e:
            log.info(str(e))

        return results

    def lists(self):
        self.initialize()
        cache = self.registry.get(LISTS_CACHE_KEY, _marker)
        if cache and cache is not _marker:
            return cache
        return self._lists()

    def subscribe(self, email, list_id, name=None, resubscribe=False):
        self.initialize()
        subscriber = Subscriber({"api_key": self.api_key})
        try:
            subscriber.add(
                list_id=list_id,
                email_address=email,
                name=name or email,
                custom_fields=[],
                resubscribe=resubscribe,
                consent_to_track="yes",
            )
            return True
        except BadRequest as e:
            log.info(str(e))
            return False

    def list_details(self, list_id):
        self.initialize()
        cm_list = List({"api_key": self.api_key}, list_id=list_id)
        details = cm_list.details()
        data = {}
        data["ConfirmationSuccessPage"] = getattr(
            details, "ConfirmationSuccessPage", None
        )
        data["ConfirmedOptIn"] = getattr(details, "ConfirmedOptIn", None)
        data["ListID"] = getattr(details, "ListID", None)
        data["Title"] = getattr(details, "Title", None)
        data["UnsubscribePage"] = getattr(details, "UnsubscribePage", None)
        data["UnsubscribeSetting"] = getattr(details, "UnsubscribeSetting", None)

        return data
