# Copyright (C) 2008, 2009 Red Hat, Inc.
# Authors: Phil Knirsch
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

import os, copy

class DiskTuning:
	def __init__(self):
		self.devidle = {}

	def __updateIdle__(self, dev, devload):
		for type in ("READ", "WRITE"):
			if devload[type] == 0.0:
				idle = self.devidle.setdefault(dev, {})
				idle.setdefault(type, 0)
				idle[type] += 1
			else:
				idle = self.devidle.setdefault(dev, {})
				idle.setdefault(type, 0)
				idle[type] = 0

	def setTuning(self, load):
		disks = load.setdefault("DISK", {})
		oldidle = copy.deepcopy(self.devidle)
		for dev in disks.keys():
			devload = disks[dev]
			self.__updateIdle__(dev, devload)
			if self.devidle[dev]["READ"] == 30 or self.devidle[dev]["WRITE"] == 30:
				os.system("hdparm -Y -S60 -B1 /dev/"+dev)
			if oldidle.has_key(dev) and oldidle[dev]["READ"] > 30 and oldidle[dev]["WRITE"] > 30 and (self.devidle[dev]["READ"] == 0 or self.devidle[dev]["WRITE"] == 0):
				os.system("hdparm -S255 -B127 /dev/"+dev)
		print(load, self.devidle)

_plugin = DiskTuning()
