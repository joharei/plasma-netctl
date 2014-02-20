# -*- coding: utf-8 -*-
#
# Author: Johan Reitan <johan.reitan@gmail.com>
# Date: Sat Jan 18 2014, 17:03:40
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as
# published by the Free Software Foundation; either version 2, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details
#
# You should have received a copy of the GNU Library General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

# Import essential modules
from PyKDE4.kdeui import KIconLoader, KIcon
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

#from __future__ import with_statement
import os
import subprocess
import re
from widget import Netctl

TIMEOUT = 5


class NetctlApplet(plasmascript.Applet):
    #   Constructor, forward initialization to its superclass
    #   Note: try to NOT modify this constructor; all the setup code
    #   should be placed in the init method.
    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)

    #   init method
    #   Put here all the code needed to initialize our plasmoid
    def init(self):
        plasmascript.Applet.init(self)
        # self.applet.setPopupIcon("network-wireless-0")

        self.setHasConfigurationInterface(False)
        self.setAspectRatioMode(Plasma.Square)

        self.theme = Plasma.Svg(self)
        # self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.StandardBackground)

        # self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
        # label = Plasma.Label(self.applet)
        # label.setText(str(wpa_status()))
        # self.layout.addItem(label)
        # self.applet.setLayout(self.layout)
        # self.resize(125, 125)

        self.widget = Netctl(self)
        self.widget.init()
        self.setGraphicsWidget(self.widget)
        self.applet.setPassivePopup(True)
        self.setPopupIcon(KIcon("network-wireless-0"))
        self.setGraphicsWidget(self.widget)

        # self.update_text()
        # self.updateIcon()


def CreateApplet(parent):
    return NetctlApplet(parent)
