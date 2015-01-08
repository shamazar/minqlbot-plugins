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

class serverelo(minqlbot.Plugin):
    def __init__(self):
        self.add_command(("serverelo", "selo"), self.cmd_serverelo)
        
        self.bot_name = minqlbot.NAME
        
        self.cache = {}

    def cmd_serverelo(self, msg, game_type, channel):
        teams = self.teams()
        balance_cache = self.plugins["balance"].cache
        players = teams["red"] + teams["blue"] + teams["spectator"]
        for name in self.cache:
            if name not in players:
                del self.cache[name]
        not_cached = self.not_cached(self.game().short_type, players)
        if not_cached:
            for player in players.copy():
                if player != self.bot_name:
                    if isinstance(player, str):
                        self.cache[player] = self.plugins["balance"].cache[player]["ca"]["elo"]
                    else:
                        self.cache[player.clean_name.lower()] = self.plugins["balance"].cache[player.clean_name.lower()]["ca"]["elo"]
        if self.bot_name in self.cache:
            del self.cache[self.bot_name]
        elos = ''
        avg = 0
        for name in self.cache:
            avg += self.cache[name]
            elos += '^7' + name + ': ^5' + str(self.cache[name]) + '^7, '
        elos = elos[:-2]
        avg /= len(self.cache)
        channel.reply("^7Average ELO: ^5{}".format(int(avg)))
        for s in self.split_long_msg(elos, delimiter=", "):
            channel.reply(s)

    def not_cached(self, game_type, player_list=None):
        not_cached = []
        teams = self.teams()
        if player_list == None:
            players = teams["red"] + teams["blue"] + teams["spectator"]
        else:
            players = player_list

        for player in players:
            if isinstance(player, str):
                if not self.is_cached(player, game_type):
                    not_cached.append(player)
            elif not self.is_cached(player.clean_name.lower(), game_type):
                not_cached.append(player.clean_name.lower())
        return not_cached

    def is_cached(self, game_type, player):
        if isinstance(player, str):
            if player in self.cache:
                return True
            else:
                return False
        else:
            if player.clean_name.lower() in self.cache:
                return True
            else:
                return False

    def split_long_msg(self, msg, limit=100, delimiter=" "):
        """Split a message into several pieces for channels with limtations."""
        if len(msg) < limit:
            return [msg]
        out = []
        index = limit
        for i in reversed(range(limit)):
            if msg[i:i + len(delimiter)] == delimiter:
                index = i
                out.append(msg[0:index])
                # Keep going, but skip the delimiter.
                rest = msg[index + len(delimiter):]
                if rest:
                    out.extend(self.split_long_msg(rest, limit, delimiter))
                return out
        out.append(msg[0:index])
        # Keep going.
        rest = msg[index:]
        if rest:
            out.extend(self.split_long_msg(rest, limit, delimiter))
        return out
