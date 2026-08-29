class IncorrectPassphraseError(Exception):
    """The supplied passphrase could not decrypt an encrypted note."""


class InvalidEncryptedNoteError(Exception):
    """An encrypted note is malformed or does not contain UTF-8 text."""


class NoteConflictError(Exception):
    """A note changed since the client last loaded it."""


class NoteEncryptionStateError(Exception):
    """An operation is incompatible with the note's encryption state."""
