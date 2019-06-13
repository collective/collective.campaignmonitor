# -*- coding: utf-8 -*-
from collective.campaignmonitor import _
from collective.campaignmonitor.interfaces import ICampaignMonitorSettings
from collective.campaignmonitor.interfaces import ICampaignMonitorConnection
from plone.app.registry.browser import controlpanel
from zope.component import getUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

try:
    from plone.protect.interfaces import IDisableCSRFProtection
except ImportError:
    # BBB for old plone.protect, default until at least Plone 4.3.7.
    IDisableCSRFProtection = None


class CampaignMonitorControlPanelForm(controlpanel.RegistryEditForm):
    schema = ICampaignMonitorSettings
    label = _("CampaingMonitor Settings")
    description = u""

    def update(self):
        self.update_cache()
        super(CampaignMonitorControlPanelForm, self).update()

    def update_cache(self):
        connection = getUtility(ICampaignMonitorConnection)
        connection.update_cache()


class CampaignMonitorControlPanel(controlpanel.ControlPanelFormWrapper):
    form = CampaignMonitorControlPanelForm
    index = ViewPageTemplateFile("controlpanel.pt")

    def campaignmonitor_account(self):
        if IDisableCSRFProtection is not None:
            alsoProvides(self.request, IDisableCSRFProtection)
        connection = getUtility(ICampaignMonitorConnection)
        if not connection.api_key:
            raise WidgetActionExecutionError(
                Invalid(
                    u"Could not fetch account details from CampaignMonitor. "
                    + u"Please check your CampaignMonitor API key: %s" % error
                )
            )
