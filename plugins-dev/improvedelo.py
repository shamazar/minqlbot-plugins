# Copyright (C) Mitch <mitch@zr.lc>

# This file is part of minqlbot.

# minqlbot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# minqlbot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with minqlbot. If not, see <http://www.gnu.org/licenses/>.

import minqlbot

class improvedelo(minqlbot.Plugin):
	def __init__(self):
		self.add_command("elo", self.cmd_elo)

	def cmd_elo(self, msg, game_type, channel):
		
