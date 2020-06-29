# -*- coding: utf-8 -*-
from collective.campaignmonitor import _  # noqa
from collective.campaignmonitor.interfaces import ICampaignMonitorConnection
from collective.campaignmonitor.interfaces import ICampaignMonitorSettings
from collective.campaignmonitor.interfaces import INewsletterSubscribe
from plone import api
from plone.registry.interfaces import IRegistry
from plone.z3cform.fieldsets import extensible
from plone.z3cform.layout import wrap_form
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import HIDDEN_MODE
from zope.component import getUtility


class NewsletterSubscribeForm(extensible.ExtensibleForm, form.Form):
    fields = field.Fields(INewsletterSubscribe)
    ignoreContext = True
    id = "cm-subscribe-form"
    label = _(u"Subscribe Form")

    def updateActions(self):
        super(NewsletterSubscribeForm, self).updateActions()
        self.actions["subscribe"].addClass("context")

    def updateWidgets(self):
        super(NewsletterSubscribeForm, self).updateWidgets()

        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ICampaignMonitorSettings)
        self.connection = getUtility(ICampaignMonitorConnection)

        # Retrieve the list id either from the request/form or fall back to
        # the default_list setting.
        list_id = self.context.REQUEST.get("list_id", None)
        list_id = list_id or self.request.form.get("form.widgets.list_id", None)
        if list_id is not None:
            self.widgets["list_id"].mode = HIDDEN_MODE
            self.widgets["list_id"].value = list_id

    @button.buttonAndHandler(
        _(u"subscribe_to_newsletter_button", default=u"Subscribe"), name="subscribe",
    )
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        list_id = data.get("list_id")
        email = data.get("email")

        resubscribe = getattr(self.settings, "force_resubscribe", False) or False

        result = self.connection.subscribe(email, list_id, resubscribe=resubscribe)
        if result:
            details = self.connection.list_details(list_id)
            if details.get("ConfirmedOptIn", None):
                message = _(
                    u"Your subscription was processed correctly. Check your e-mail for a confirmation message."
                )
            else:
                message = _(u"You have been subscribed to the newsletter")
            api.portal.show_message(message, request=self.request, type="info")
        else:
            message = _(u"Your subscription could not be processed. Please try again.")
            api.portal.show_message(message, request=self.request, type="error")

        self.request.response.redirect(self.context.absolute_url())


NewsletterSubscribeView = wrap_form(NewsletterSubscribeForm)
