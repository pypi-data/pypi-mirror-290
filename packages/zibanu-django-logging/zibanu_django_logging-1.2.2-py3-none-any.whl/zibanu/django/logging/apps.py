# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         10/12/22 10:23 AM
# Project:      Zibanu Django Project
# Module Name:  apps
# Description:
# ****************************************************************
import logging
import threading
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from zibanu.django.logging.lib import signals_factory


class ZbDjangoLogging(AppConfig):
    """
    Inherited class from django.apps.AppConfig to define configuration of zibanu.django.logging app.
    """
    default_auto_field = "django.db.models.AutoField"
    name = "zibanu.django.logging"
    verbose_name = _("Zibanu Logging")
    label = "zb_logging"

    def ready(self):
        """
        Override method used for django application loader after the application has been loaded successfully.
        """
        # Call a thread to wait app ready to load signals.
        t1 = threading.Thread(target=self.after_ready, name="after ready event")
        t1.start()

    def after_ready(self):
        """
        After ready thread event to call signals factory.

        Returns
        -------
        None
        """
        # Wait for ready_event
        event_is_set = self.apps.ready_event.wait()
        if event_is_set and self.apps.ready:
            signals_factory()
