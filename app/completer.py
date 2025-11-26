class Completer:
    def __init__(self, commands: list[str]):
        # Ensure commands is a list of keys (strings), not a dict_keys object
        self.commands = sorted(list(commands))
        self.matches = None

    def completer(self, text: str, state: int) -> str | None:
        """Tab completion for builtin commands and files."""
        # Print statements are helpful for debugging, but we can refine the logic.

        # When state is 0, we find all matches for the current 'text' prefix.
        if state == 0:
            self.matches = [cmd for cmd in self.commands if cmd.startswith(text)]
            # Also consider file path completion here if you want:
            # self.matches.extend(glob.glob(text + '*'))

        # Return the match for the current state, or None if no more matches.
        try:
            return self.matches[state]
        except IndexError:
            return None
