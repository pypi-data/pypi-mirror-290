# -*- coding: utf-8 -*-
"""
Interfaces for visaplan.plone.infohubs
"""

from __future__ import absolute_import

# Zope:
from zope.interface import Interface


class IHubAndInfo(Interface):
    def get():
        """
        Erzeuge hub und info für den aktuellen Kontext und gib ein dict zurück
        """


class IInfohubsDemo(Interface):
    """
    Feed @@infohubs-demo
    """
