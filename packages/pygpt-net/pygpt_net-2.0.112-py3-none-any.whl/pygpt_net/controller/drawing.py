#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.01.18 10:00:00                  #
# ================================================== #

import datetime
import os

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QImage

from pygpt_net.utils import trans


class Drawing:
    def __init__(self, window=None):
        """
        Drawing controller

        :param window: Window instance
        """
        self.window = window

    def setup(self):
        """Setup drawing"""
        self.restore_current()
        size = "800x600"  # default size
        if self.window.core.config.has('painter.canvas.size'):
            size = self.window.core.config.get('painter.canvas.size')
        self.window.ui.nodes['painter.select.canvas.size'].setCurrentText(size)
        self.change_canvas_size(size)

    def is_drawing(self) -> bool:
        """
        Check if drawing is enabled

        :return: True if drawing is current active tab
        """
        return self.window.controller.ui.current_tab == self.window.controller.ui.tab_idx['draw']

    def convert_to_size(self, canvas_size: str) -> tuple:
        """
        Convert string to size

        :param canvas_size: Canvas size string
        :return: tuple (width, height)
        """
        return tuple(map(int, canvas_size.split('x'))) if canvas_size else (0, 0)

    def set_canvas_size(self, width: int, height: int):
        """
        Set canvas size

        :param width: int
        :param height: int
        """
        self.window.ui.painter.setFixedSize(QSize(width, height))

    def open(self, path):
        """
        Open image

        :param path: str
        """
        self.window.ui.painter.open_image(path)

    def from_camera(self):
        """Get image from camera"""
        if not self.window.controller.camera.is_enabled():
            self.window.controller.camera.enable_capture()
            self.window.controller.camera.setup_ui()
        frame = self.window.controller.camera.get_current_frame(False)
        if frame is None:
            return
        height, width, channel = frame.shape
        bytes = 3 * width
        image = QImage(frame.data, width, height, bytes, QImage.Format_RGB888)
        self.window.ui.painter.set_image(image)

    def restore_current(self):
        """Restore previous image"""
        path = os.path.join(self.window.core.config.get_user_dir('capture'), '_current.png')
        if os.path.exists(path):
            self.window.ui.painter.image.load(path)
            self.window.ui.painter.update()

    def save_all(self):
        """Save all (on exit)"""
        self.save_current()

    def save_current(self):
        """Store current image"""
        path = os.path.join(self.window.core.config.get_user_dir('capture'), '_current.png')
        self.window.ui.painter.image.save(path)

    def set_brush_mode(self, enabled: bool):
        """
        Set the paint mode

        :param enabled: bool
        """
        if enabled:
            self.window.ui.nodes['painter.select.brush.color'].setCurrentText("Black")
            self.window.ui.painter.set_brush_color(Qt.black)

    def set_erase_mode(self, enabled: bool):
        """
        Set the erase mode

        :param enabled: bool
        """
        if enabled:
            self.window.ui.nodes['painter.select.brush.color'].setCurrentText("White")
            self.window.ui.painter.set_brush_color(Qt.white)

    def change_canvas_size(self, selected=None):
        """
        Change the canvas size

        :param selected: Selected size
        """
        if not selected:
            selected = self.window.ui.nodes['painter.select.canvas.size'].currentData()
        if selected:
            size = self.convert_to_size(selected)
            self.set_canvas_size(size[0], size[1])
            self.window.core.config.set('painter.canvas.size', selected)
            self.window.core.config.save()

    def change_brush_size(self, size):
        """
        Change the brush size

        :param size: Brush size
        """
        self.window.ui.painter.set_brush_size(int(size))

    def change_brush_color(self):
        """Change the brush color"""
        color = self.window.ui.nodes['painter.select.brush.color'].currentData()
        self.window.ui.painter.set_brush_color(color)

    def attach(self, name: str, path: str, type: str = 'drawing'):
        """
        Attach image to attachments

        :param name: image name
        :param path: image path
        :param type: capture type
        """
        mode = self.window.core.config.get('mode')
        if type == 'drawing':
            title = trans('painter.capture.name.prefix') + ' ' + name
        elif type == 'screenshot':
            title = trans('screenshot.capture.name.prefix') + ' ' + name
        else:
            title = name
        title = title.replace('cap-', '').replace('_', ' ')
        self.window.core.attachments.new(mode, title, path, False)
        self.window.core.attachments.save()
        self.window.controller.attachment.update()

    def capture(self):
        """Capture current image"""
        # switch to vision mode if needed
        self.window.controller.chat.vision.switch_to_vision()

        # clear attachments before capture if needed
        if self.window.controller.attachment.is_capture_clear():
            self.window.controller.attachment.clear(True)

        try:
            # prepare filename
            now = datetime.datetime.now()
            dt = now.strftime("%Y-%m-%d_%H-%M-%S")
            name = 'cap-' + dt
            path = os.path.join(self.window.core.config.get_user_dir('capture'), name + '.png')

            # capture
            self.window.ui.painter.image.save(path)
            self.attach(name, path)

            # show last capture time in status
            dt_info = now.strftime("%Y-%m-%d %H:%M:%S")
            self.window.statusChanged.emit(trans("painter.capture.manual.captured.success") + ' ' + dt_info)
            return True

        except Exception as e:
            print("Image capture exception", e)
            self.window.core.debug.log(e)

    def make_screenshot(self):
        """Make screenshot and append to attachments"""
        # switch to vision mode if needed
        self.window.controller.chat.vision.switch_to_vision()

        # clear attachments before capture if needed
        if self.window.controller.attachment.is_capture_clear():
            self.window.controller.attachment.clear(True)

        try:
            # prepare filename
            now = datetime.datetime.now()
            dt = now.strftime("%Y-%m-%d_%H-%M-%S")
            name = 'cap-' + dt
            path = os.path.join(self.window.core.config.get_user_dir('capture'), name + '.png')

            # capture screenshot
            screen = self.window.app.primaryScreen()
            screenshot = screen.grabWindow(0)
            screenshot.save(path, 'png')
            self.attach(name, path, 'screenshot')
            self.open(path)

            # show last capture time in status
            dt_info = now.strftime("%Y-%m-%d %H:%M:%S")
            self.window.statusChanged.emit(trans("painter.capture.manual.captured.success") + ' ' + dt_info)
            return True

        except Exception as e:
            print("Screenshot capture exception", e)
            self.window.core.debug.log(e)

    def get_colors(self) -> dict:
        """
        Get colors dict

        :return: colors dict
        """
        return {
            "Black": Qt.black,
            "White": Qt.white,
            "Red": Qt.red,
            "Orange": QColor('orange'),
            "Yellow": Qt.yellow,
            "Green": Qt.green,
            "Blue": Qt.blue,
            "Indigo": QColor('indigo'),
            "Violet": QColor('violet')
        }

    def get_sizes(self) -> list:
        """
        Get brush sizes

        :return: list of sizes
        """
        return ['1', '2', '3', '5', '8', '12', '15', '20', '25', '30', '50', '100', '200']

    def get_canvas_sizes(self) -> list:
        """
        Get canvas sizes

        :return: list of sizes
        """
        return [
            "640x480", "800x600", "1024x768", "1280x720", "1600x900",
            "1920x1080", "2560x1440", "3840x2160", "4096x2160"
        ]
