# -*- coding: utf-8 -*-
from collective.campaignmonitor import _
from collective.campaignmonitor.interfaces import ICampaignMonitorSettings
from plone.app.registry.browser import controlpanel
from collective.campaignmonitor.interfaces import ICampaignMonitorConnection

class CampaignMonitorControlPanel(controlpanel.RegistryEditForm):
    schema = ICampaignMonitorSettings
    label = _('CampaingMonitor Settings')
    description = u''

    def update(self):
        self.update_cache()
        super(CampaignMonitorControlPanel, self).update()

    def update_cache(self):
        cm = getUtility(ICampaignMonitorConnection)
        cm.update_cache()
