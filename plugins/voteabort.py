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

"""
Allows the players to vote to abort the game using !abort and !y to agree.

REQUIRES COMMENTING OUT ABORT COMMAND IN ESSENTIALS
"""

import minqlbot

class voteabort(minqlbot.Plugin):
    def __init__(self):
        self.add_hook("game_start", self.handle_game_start)
        self.add_hook("round_end", self.handle_round_end)
        self.add_command("abort", self.cmd_abort)
        self.add_command(("yes", "y"), self.cmd_vote_abort)

    def handle_game_start(self, game):
        self.abort_votes = 0
        self.vote_in_progress = False
        self.voted = []

    def handle_round_end(self, score, winner):
        self.abort_votes = 0
        self.vote_in_progress = False
        self.voted = []

    def cmd_abort(self, player, msg, channel):
        teams = self.teams()
        players = teams["red"] + teams["blue"]
        if self.game().state == "in_progress":
            if self.has_permission(player, 2):
                self.abort_game(channel)
            else:
                if player in players:
                    self.vote_in_progress = True
                    self.voted.append(player)
                    channel.reply("^7Abort vote started. Vote with ^5!y ^7before the next round starts.")
                    if len(players) == 2:
                        self.required = 2
                    else:
                        self.required = float(len(players))*0.7
                else:
                    channel.reply("^7You aren't playing in this game!")
        else:
            channel.reply("^7But the game isn't even on!")

    def cmd_vote_abort(self, player, msg, channel):
        teams = self.teams()
        players = teams["red"] + teams["blue"]
        if self.game().state == "in_progress":
            if self.vote_in_progress:
                if player in players:
                    if player in self.voted:
                        channel.reply("^7You've already voted!")
                    else:
                        self.abort_votes += 1
                        self.voted.append(player)
                        if self.abort_votes >= int(self.required):
                            self.abort_game(channel)
                        else:
                            channel.reply("^5{} ^7votes out of ^5{}^7.".format(self.abort_votes, int(self.required)))
                else:
                    channel.replay("^7You aren't playing in this game!")
        else:
            channel.reply("^7But the game isn't even on!")


    def abort_game(self, channel):
        if self.game().state == "in_progress":
            self.abort()
        else:
            channel.reply("^7But the game isn't even on!")