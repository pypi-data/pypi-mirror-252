#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.01.13 10:00:00                  #
# ================================================== #

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QRadioButton, QPushButton, QComboBox, QScrollArea

from pygpt_net.ui.widget.draw.painter import PainterWidget
from pygpt_net.ui.widget.element.help import HelpLabel
from pygpt_net.utils import trans


class Painter:
    def __init__(self, window=None):
        """
        Painter UI

        :param window: Window instance
        """
        self.window = window

    def setup(self) -> QWidget:
        """
        Setup painter

        :return: QWidget
        """
        widget = QWidget()
        widget.setLayout(self.setup_painter())

        return widget

    def setup_painter(self) -> QVBoxLayout:
        """
        Setup painter

        :return: QVBoxLayout
        """
        self.window.ui.painter = PainterWidget(self.window)

        top = QHBoxLayout()

        self.window.ui.nodes['painter.btn.brush'] = QRadioButton(trans('painter.mode.paint'))
        self.window.ui.nodes['painter.btn.brush'].setChecked(True)
        self.window.ui.nodes['painter.btn.brush'].toggled.connect(self.window.controller.drawing.set_brush_mode)
        top.addWidget(self.window.ui.nodes['painter.btn.brush'])

        self.window.ui.nodes['painter.btn.erase'] = QRadioButton(trans('painter.mode.erase'))
        self.window.ui.nodes['painter.btn.erase'].toggled.connect(self.window.controller.drawing.set_erase_mode)
        top.addWidget(self.window.ui.nodes['painter.btn.erase'])

        sizes = self.window.controller.drawing.get_sizes()
        self.window.ui.nodes['painter.select.brush.size'] = QComboBox()
        self.window.ui.nodes['painter.select.brush.size'].addItems(sizes)
        self.window.ui.nodes['painter.select.brush.size'].currentTextChanged.connect(
            self.window.controller.drawing.change_brush_size)
        self.window.ui.nodes['painter.select.brush.size'].setMinimumContentsLength(10)
        self.window.ui.nodes['painter.select.brush.size'].setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.window.ui.nodes['painter.select.brush.size'].setCurrentIndex(
            self.window.ui.nodes['painter.select.brush.size'].findText('3'))
        top.addWidget(self.window.ui.nodes['painter.select.brush.size'])

        self.window.ui.nodes['painter.select.brush.color'] = QComboBox()
        colors = self.window.controller.drawing.get_colors()
        for color_name, color_value in colors.items():
            self.window.ui.nodes['painter.select.brush.color'].addItem(color_name, color_value)
        self.window.ui.nodes['painter.select.brush.color'].currentTextChanged.connect(
            self.window.controller.drawing.change_brush_color)
        self.window.ui.nodes['painter.select.brush.color'].setMinimumContentsLength(10)
        self.window.ui.nodes['painter.select.brush.color'].setSizeAdjustPolicy(QComboBox.AdjustToContents)
        top.addWidget(self.window.ui.nodes['painter.select.brush.color'])

        canvas_sizes = self.window.controller.drawing.get_canvas_sizes()
        self.window.ui.nodes['painter.select.canvas.size'] = QComboBox()
        self.window.ui.nodes['painter.select.canvas.size'].addItems(canvas_sizes)
        self.window.ui.nodes['painter.select.canvas.size'].setMinimumContentsLength(20)
        self.window.ui.nodes['painter.select.canvas.size'].setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.window.ui.nodes['painter.select.canvas.size'].currentTextChanged.connect(
            self.window.controller.drawing.change_canvas_size)
        top.addWidget(self.window.ui.nodes['painter.select.canvas.size'])

        top.addStretch(1)
        self.window.ui.nodes['painter.btn.capture'] = QPushButton(trans('painter.btn.capture'))
        self.window.ui.nodes['painter.btn.capture'].clicked.connect(self.window.controller.drawing.capture)
        top.addWidget(self.window.ui.nodes['painter.btn.capture'])

        self.window.ui.nodes['painter.btn.camera.capture'] = QPushButton(trans('painter.btn.camera.capture'))
        self.window.ui.nodes['painter.btn.camera.capture'].clicked.connect(self.window.controller.drawing.from_camera)
        top.addWidget(self.window.ui.nodes['painter.btn.camera.capture'])

        self.window.ui.nodes['painter.btn.clear'] = QPushButton(trans('painter.btn.clear'))
        self.window.ui.nodes['painter.btn.clear'].clicked.connect(self.window.ui.painter.clear_image)
        top.addWidget(self.window.ui.nodes['painter.btn.clear'])

        self.window.ui.painter_scroll = QScrollArea()
        self.window.ui.painter_scroll.setWidget(self.window.ui.painter)
        self.window.ui.painter_scroll.setWidgetResizable(True)

        self.window.ui.nodes['tip.output.tab.draw'] = HelpLabel(trans('tip.output.tab.draw'), self.window)

        layout = QVBoxLayout()

        layout.addLayout(top)
        layout.addWidget( self.window.ui.painter_scroll)
        layout.addWidget(self.window.ui.nodes['tip.output.tab.draw'])
        layout.setContentsMargins(0, 0, 0, 0)

        return layout



