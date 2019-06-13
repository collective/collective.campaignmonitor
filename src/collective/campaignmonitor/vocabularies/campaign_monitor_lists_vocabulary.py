# -*- coding: utf-8 -*-

# from plone import api
from collective.campaignmonitor import _
from plone.dexterity.interfaces import IDexterityContent
from collective.campaignmonitor.interfaces import ICampaingMonitorConnection
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getUtility


@implementer(IVocabularyFactory)
class CampaignMonitorListsVocabulary(object):
    """
    """

    def __call__(self, context):
        connection = getUtility(ICampaingMonitorConnection)
        items = connection.lists()

        terms = []
        for item in items:
            terms.append(
                SimpleTerm(
                    value=item.get("list_id"),
                    token=str(item.get("list_id")),
                    title=item.get("list_name"),
                )
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


CampaignMonitorListsVocabularyFactory = CampaignMonitorListsVocabulary()
