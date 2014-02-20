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

TIMEOUT = 5


class Netctl(QGraphicsWidget):
    def __init__(self, parent):
        QGraphicsWidget.__init__(self)
        self.applet = parent

    def init(self):
        # self.applet.setPopupIcon("network-wireless-0")

        # self.setHasConfigurationInterface(False)
        # self.setAspectRatioMode(Plasma.Square)

        # self.theme = Plasma.Svg(self)
        # self.theme.setImagePath("widgets/background")
        # self.setBackgroundHints(Plasma.Applet.DefaultBackground)

        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self)
        self.label = Plasma.Label(self)
        self.label.setText('{!s}\nStrength: {:.2f} %'.format(wpa_status(), get_quality()))
        self.layout.addItem(self.label)
        self.setLayout(self.layout)
        self.resize(125, 125)

        self.counter = 0

        # self.setPopupIcon(KIcon("network-wireless-0"))

        self.update_loop()
        self.update_icon()

    @pyqtSlot()
    def update_loop(self):
        try:
            self.update_text()
            self.update_icon()
        finally:
            QTimer.singleShot(5000, self.update_loop)

    def update_text(self):
        self.label.setText('{!s}\nStrength: {:.2f} %'.format(wpa_status(), get_quality()))

    def update_icon(self):
        quality = get_quality()
        print("Quality: {}".format(quality))
        if quality >= 100:
            self.applet.setPopupIcon("network-wireless-100")
        elif quality >= 80:
            self.applet.setPopupIcon("network-wireless-80")
        elif quality >= 75:
            self.applet.setPopupIcon("network-wireless-75")
        elif quality >= 60:
            self.applet.setPopupIcon("network-wireless-60")
        elif quality >= 50:
            self.applet.setPopupIcon("network-wireless-50")
        elif quality >= 40:
            self.applet.setPopupIcon("network-wireless-40")
        elif quality >= 25:
            self.applet.setPopupIcon("network-wireless-25")
        elif quality >= 20:
            self.applet.setPopupIcon("network-wireless-20")
        else:
            self.applet.setPopupIcon("network-wired")


def get_quality():
    stdout = subprocess.check_output(['iwconfig'], stderr=open(os.devnull, 'wb'))
    quality = ''
    for line in stdout.split('\n'):
        if 'Quality' in line:
            quality = line
            break
    qmax = int(quality[26:28])
    q = int(quality[23:25])
    return 1. * q / qmax * 100


def default_interface():
    """returns the interface of the default route"""
    interface = None
    stdout = subprocess.check_output(['ip', 'route', 'list', 'scope', 'global'])
    for line in stdout.split('\n'):
        route = line.split(' ')
        if len(route) >= 5 and (route[0], route[1], route[3]) == ('default', 'via', 'dev'):
            interface = route[4]
            break
    return interface


def carrier_ok(iface):
    """check if the interface is connected"""
    iface_dir = '/sys/class/net/%s' % iface
    with open(iface_dir + '/carrier') as f:
        line = f.next().strip()
        return line == '1'


def wpa_status():
    """returns the output of wpa_cli status."""
    return subprocess.check_output(['wpa_cli', 'status']).strip()


def eth_status(iface):
    """returns the status of the given interface (for the tooltip)"""
    stdout = subprocess.check_output(['ip', 'addr', 'show', 'dev', iface])
    res = ''
    for line in stdout.split('\n'):
        m = re.search('(inet6? [^ ]*) ', line)
        if m:
            res = '\n'.join([res, m.group(1)])
    return res


def interface_type(iface):
    """http://stackoverflow.com/questions/4475420/detect-network-connection-type-in-linux/16060638#16060638)"""
    res = 'wired'
    iface_dir = '/sys/class/net/%s' % iface
    with open(iface_dir + '/type') as f:
        line = f.next().strip()
        if line == '1':
            res = 'wired'
            if 'wireless' in os.listdir(iface_dir) or 'phy80211' in os.listdir(iface_dir):
                res = 'wireless'
    return res