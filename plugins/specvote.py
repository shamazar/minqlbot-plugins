import minqlbot

class specvote(minqlbot.Plugin):
	def __init__(self):
		self.add_hook("vote_called", self.handle_vote_called)

	def handle_vote_called(self, caller, vote, args):
		specs = self.teams()["spectator"]
		if caller.clean_name.lower() in specs:
			if not self.has_permission(caller, 1):
				self.vote_no()
				self.msg("^7Specs are not allowed to vote.")
