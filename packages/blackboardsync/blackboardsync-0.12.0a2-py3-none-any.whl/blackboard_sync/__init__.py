#!/usr/bin/env python3

"""
BlackboardSync
~~~~~~~~~~

Keep your Blackboard files synced locally

:copyright: (c) 2023, Jacob Sánchez Pérez.
:license: GPL v2.0, see LICENSE for details.
"""

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.
# Also available at https://www.gnu.org/licenses/old-licenses/gpl-2.0.html

import logging

from .__about__ import __title__, __summary__, __uri__
from .__about__ import __author__, __email__, __license__
from .__about__ import __copyright__


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
