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

class lockteams(minqlbot.Plugin):
    def __init__(self):
        self.add_hook("chat", self.handle_chat)
        self.add_hook("console", self.handle_console)
        self.add_hook("map", self.handle_map)
        self.add_command("lock", self.cmd_lock, 1)
        self.add_command("unlock", self.cmd_unlock, 1)

        self.red_locked = False
        self.blue_locked = False

    def handle_chat(self, player, msg, chat_type):
        if "lock" in msg:
            if self.game().state == "warmup":
                if self.red_locked and self.blue_locked:
                    self.send_command("unlock")

    def handle_console(self, cmd):
        if "The RED team is now locked" in cmd:
            self.red_locked = True
        elif "The BLUE team is now locked" in cmd:
            self.blue_locked = True
        elif "The RED team is now unlocked" in cmd:
            self.red_locked = False
        elif "The RED team is now unlocked" in cmd:
            self.blue_locked = False

    def handle_map(self, map):
        self.red_locked = False
        self.blue_locked = False

    def cmd_lock(self, player, msg, channel):
        if len(msg) < 2:
            self.send_command("lock")
        elif msg[1] == "r":
            self.send_command("lock r")
        elif msg[1] == "b":
            self.send_command("lock b")
        else:
            channel.reply("^7Unintelligible input.")

    def cmd_unlock(self, player, msg, channel):
        if len(msg) < 2:
            self.send_command("unlock")
        elif msg[1] == "r":
            self.send_command("unlock r")
        elif msg[1] == "b":
            self.send_command("unlock b")
        else:
            channel.reply("^7Unintelligible input.")