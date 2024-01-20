#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.01.08 17:00:00                  #
# ================================================== #

from PySide6.QtCore import QObject, Signal, QRunnable, Slot

from pygpt_net.core.dispatcher import Event
from pygpt_net.item.ctx import CtxItem
from pygpt_net.utils import trans


class BasePlugin:
    def __init__(self, *args, **kwargs):
        self.window = kwargs.get('window', None)
        self.id = ""
        self.name = ""
        self.type = []  # audio.input, audio.output, text.input, text.output, image.input, image.output
        self.description = ""
        self.urls = {}
        self.options = {}
        self.initial_options = {}
        self.parent = None
        self.enabled = False
        self.use_locale = False
        self.is_async = False
        self.order = 0

    def setup(self):
        """
        Return available config options

        :return: config options
        :rtype: dict
        """
        return self.options

    def add_option(self,
                   name: str,  # option name (ID, key)
                   type: str,  # option type (text, textarea, bool, int, float, dict)
                   value: any = None,  # option value
                   label: str = "",  # option label
                   description: str = "",  # option description
                   tooltip: str = None,  # option tooltip
                   min: int = None,  # option min value
                   max: int = None,  # option max value
                   multiplier: int = 1,  # option float value multiplier (for sliders)
                   step: int = 1,  # option step value (for sliders)
                   slider: bool = False,  # option slider (True/False)
                   keys: dict or list = None,  # option keys dict (dict type) or key-value pairs list (combo type)
                   advanced: bool = False,  # option is advanced (True/False)
                   secret: bool = False,  # option is secret (True/False)
                   persist: bool = False,  # option is persistent on reset to defaults (True/False)
                   urls: dict = None,  # option URLs (API keys, docs, etc.)
                   use: str = None):  # placeholders to use in combo type items
        """
        Add plugin configuration option

        :param name: Option name (ID, key)
        :param type: Option type (text, textarea, bool, int, float, dict)
        :param value: Option value
        :param label: Option label
        :param description: Option description
        :param tooltip: Option tooltip
        :param min: Option min value
        :param max: Option max value
        :param multiplier: Option float value multiplier
        :param step: Option step value (for slider)
        :param slider: Option slider (True/False)
        :param keys: Option keys (for dict type)
        :param advanced: Option advanced (True/False)
        :param secret: Option secret (True/False)
        :param persist: Option persist (True/False)
        :param urls: Option URLs
        :param use: Placeholders to use in combo type
        """
        if tooltip is None:
            tooltip = description

        option = {
            "id": name,  # append ID based on name
            "type": type,
            "value": value,
            "label": label,
            "description": description,
            "tooltip": tooltip,
            "min": min,
            "max": max,
            "multiplier": multiplier,
            "step": step,
            "slider": slider,
            "keys": keys,
            "advanced": advanced,
            "secret": secret,
            "persist": persist,
            "urls": urls,
            "use": use,
        }
        self.options[name] = option

    def has_option(self, name: str) -> bool:
        """
        Check if option exists

        :param name: option name
        :return: True if exists
        :rtype: bool
        """
        return name in self.options

    def get_option(self, name: str) -> dict:
        """
        Return option

        :param name: option name
        :return: option
        :rtype: dict
        """
        if self.has_option(name):
            return self.options[name]

    def get_option_value(self, name: str) -> any:
        """
        Return option value

        :param name: option name
        :return: option value
        :rtype: any
        """
        if self.has_option(name):
            return self.options[name]["value"]

    def attach(self, window):
        """
        Attach window to plugin

        :param window: Window instance
        """
        self.window = window

    def handle(self, event: Event, *args, **kwargs):
        """
        Handle event

        :param event: event name
        :param args: arguments
        :param kwargs: keyword arguments
        """
        return

    def on_update(self, *args, **kwargs):
        """
        Called on update

        :param args: arguments
        :param kwargs: keyword arguments
        """
        return

    def on_post_update(self, *args, **kwargs):
        """
        Called on post-update

        :param args: arguments
        :param kwargs: keyword arguments
        """
        return

    def trans(self, text: str = None) -> str:
        """
        Translate text using plugin domain

        :param text: text to translate
        :return: translated text
        :rtype: str
        """
        if text is None:
            return ""
        domain = 'plugin.{}'.format(self.id)
        return trans(text, False, domain)

    def error(self, err: any):
        """
        Send error message to logger

        :param err: error message
        """
        self.window.core.debug.log(err)
        self.window.controller.debug.log(str(err), True)
        self.window.ui.dialogs.alert("{}: {}".format(self.name, err))

    def debug(self, data: any):
        """
        Send debug message to logger window

        :param data: data to send
        """
        self.window.controller.debug.log(data, True)

    def log(self, msg: str):
        """
        Log message to logger and console

        :param msg: message to log
        """
        self.debug(msg)
        self.window.ui.status(msg)
        print(msg)

    @Slot(object, object)
    def handle_finished(self, response: dict, ctx: CtxItem = None):
        """
        Handle finished response signal

        :param response: response
        :param ctx: context (CtxItem)
        """
        # dispatcher handle late response
        if ctx is not None:
            ctx.results.append(response)
            ctx.reply = True
            self.window.core.dispatcher.reply(ctx)

    @Slot(object)
    def handle_status(self, data: str):
        """
        Handle thread status msg signal

        :param data: status message
        """
        self.window.ui.status(str(data))

    @Slot(object)
    def handle_error(self, err: any):
        """
        Handle thread error signal

        :param err: error message
        """
        self.error(err)

    @Slot(object)
    def handle_debug(self, msg: any):
        """
        Handle debug message signal

        :param msg: debug message
        """
        self.debug(msg)

    @Slot(object)
    def handle_log(self, msg: str):
        """
        Handle log message signal

        :param msg: log message
        """
        self.log(msg)


class BaseSignals(QObject):
    finished = Signal(object, object)  # response, ctx
    debug = Signal(object)
    destroyed = Signal()
    error = Signal(object)
    log = Signal(object)
    started = Signal()
    status = Signal(object)
    stopped = Signal()


class BaseWorker(QRunnable):
    def __init__(self, *args, **kwargs):
        super(BaseWorker, self).__init__()
        self.signals = BaseSignals()
        self.args = args
        self.kwargs = kwargs
        self.plugin = None
        self.cmds = None
        self.ctx = None

    def debug(self, msg):
        if self.signals is not None and hasattr(self.signals, "debug"):
            self.signals.debug.emit(msg)

    def destroyed(self):
        if self.signals is not None and hasattr(self.signals, "destroyed"):
            self.signals.destroyed.emit()

    def error(self, err):
        if self.signals is not None and hasattr(self.signals, "error"):
            self.signals.error.emit(err)

    def log(self, msg):
        if self.signals is not None and hasattr(self.signals, "log"):
            self.signals.log.emit(msg)

    def response(self, response):
        if self.signals is not None and hasattr(self.signals, "finished"):
            self.signals.finished.emit(response, self.ctx)

    def started(self):
        if self.signals is not None and hasattr(self.signals, "started"):
            self.signals.started.emit()

    def status(self, msg):
        if self.signals is not None and hasattr(self.signals, "status"):
            self.signals.status.emit(msg)

    def stopped(self):
        if self.signals is not None and hasattr(self.signals, "stopped"):
            self.signals.stopped.emit()
            