from app.utils import find_executables_in_path


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
            builtin_matches = [cmd for cmd in self.commands if cmd.startswith(text)]
            # Also consider file path completion here if you want:
            # self.matches.extend(glob.glob(text + '*'))
            external_matches = find_executables_in_path(text)

            combined_matches = set(builtin_matches) | external_matches
            self.matches = sorted(list(combined_matches))

        # Return the match for the current state, or None if no more matches.
        try:
            match = self.matches[state]

            # --- THIS IS THE NEW LOGIC ---
            # If there's only one possible match, add a space.
            if len(self.matches) == 1:
                return match + " "
            # If there are multiple matches, return the plain word.
            # The display hook will handle formatting.
            else:
                return match

        except IndexError:
            return None
