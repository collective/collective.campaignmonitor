# -*- coding: utf-8 -*-
from collective.campaignmonitor import _
from collective.campaignmonitor.interfaces import ICampaignMonitorConnection
from collective.campaignmonitor.interfaces import ICampaignMonitorSettings
from plone.app.registry.browser import controlpanel
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.interfaces import WidgetActionExecutionError
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import Invalid


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
        if IDisableCSRFProtection is not None:
            alsoProvides(self.request, IDisableCSRFProtection)

        self.update_cache()
        super(CampaignMonitorControlPanelForm, self).update()

    def update_cache(self):
        connection = getUtility(ICampaignMonitorConnection)
        connection.update_cache()


class CampaignMonitorControlPanel(controlpanel.ControlPanelFormWrapper):
    form = CampaignMonitorControlPanelForm
    index = ViewPageTemplateFile("controlpanel.pt")

    def campaignmonitor_account(self):
        # if IDisableCSRFProtection is not None:
        #     alsoProvides(self.request, IDisableCSRFProtection)
        connection = getUtility(ICampaignMonitorConnection)
        try:
            return connection.account()
        except Exception as e:
            raise WidgetActionExecutionError(
                Invalid(
                    "Could not fetch account details from CampaignMonitor. Please check your CampaignMonitor API key: {0}".format(
                        e
                    )
                )
            )
