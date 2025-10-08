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
class CampaignMonitorConnection:
    def __init__(self):
        self.api_key = None

    def initialize(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICampaignMonitorSettings)
        self.api_key = settings.api_key

        return registry, settings

    def account(self):
        self.initialize()
        return self.api_key

    def update_cache(self):
        log.info("Updating cache...")
        registry, settings = self.initialize()
        if not settings.api_key:
            return

        clients = self._clients()
        if type(clients) is list:
            clients = tuple(clients)
            if registry[CLIENTS_CACHE_KEY] != clients:
                registry[CLIENTS_CACHE_KEY] = clients
                log.info("Updated client list.")

        lists = self._lists()
        if type(lists) is list:
            lists = tuple(lists)
            if registry[LISTS_CACHE_KEY] != lists:
                registry[LISTS_CACHE_KEY] = lists
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
        registry, settings = self.initialize()
        cache = registry.get(CLIENTS_CACHE_KEY, _marker)
        if cache and cache is not _marker:
            return cache
        return self._clients()

    def _lists(self):
        registry, settings = self.initialize()
        cs = Client({"api_key": self.api_key}, settings.client_id)
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
        registry, settings = self.initialize()
        cache = registry.get(LISTS_CACHE_KEY, _marker)
        if cache and cache is not _marker:
            return cache
        return self._lists()

    def subscribe(self, email, list_id, name=None, custom_fields=[], resubscribe=False):
        self.initialize()
        subscriber = Subscriber({"api_key": self.api_key})
        try:
            subscriber.add(
                list_id=list_id,
                email_address=email,
                name=name or email,
                custom_fields=custom_fields,
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

    def get_subscriber(self, list_id, email_address):
        self.initialize()
        subscriber = Subscriber({"api_key": self.api_key})
        try:
            return subscriber.get(list_id=list_id, email_address=email_address)
        except BadRequest as e:
            log.info(str(e))
            return False

    def list_webhooks(self, list_id):
        self.initialize()
        cm_list = List({"api_key": self.api_key}, list_id=list_id)
        return cm_list.webhooks()

    def create_list_webhook(self, list_id, events, url, payload_format="json"):
        self.initialize()
        cm_list = List({"api_key": self.api_key}, list_id=list_id)
        try:
            cm_list.create_webhook(events, url, payload_format)
            return True
        except BadRequest as e:
            log.info(str(e))
            return False

    def delete_list_webhook(self, list_id, webhook_id):
        self.initialize()
        cm_list = List({"api_key": self.api_key}, list_id=list_id)
        try:
            cm_list.delete_webhook(webhook_id)
            return True
        except BadRequest as e:
            log.info(str(e))
            return False
