# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.campaignmonitor


class CollectiveCampaignmonitorLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.campaignmonitor)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.campaignmonitor:default')


COLLECTIVE_CAMPAIGNMONITOR_FIXTURE = CollectiveCampaignmonitorLayer()


COLLECTIVE_CAMPAIGNMONITOR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CAMPAIGNMONITOR_FIXTURE,),
    name='CollectiveCampaignmonitorLayer:IntegrationTesting',
)


COLLECTIVE_CAMPAIGNMONITOR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CAMPAIGNMONITOR_FIXTURE,),
    name='CollectiveCampaignmonitorLayer:FunctionalTesting',
)


COLLECTIVE_CAMPAIGNMONITOR_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_CAMPAIGNMONITOR_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveCampaignmonitorLayer:AcceptanceTesting',
)
