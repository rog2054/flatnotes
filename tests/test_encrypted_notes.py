from pathlib import Path

import pytest
from pyrage import passphrase as age_passphrase

from notes.errors import (
    IncorrectPassphraseError,
    InvalidEncryptedNoteError,
    NoteConflictError,
)
from notes.file_system.file_system import AGE_ARMOR_HEADER, FileSystemNotes
from notes.models import NoteCreate, NoteSecret, NoteUpdate

PASSPHRASE = "correct horse battery staple"
CONTENT = "# Private\n\nA secret with #private-tag and Unicode: café 🔐"


@pytest.fixture
def notes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("FLATNOTES_PATH", str(tmp_path))
    return FileSystemNotes()


def create_private_note(notes: FileSystemNotes):
    return notes.create(NoteCreate(title="Private Plan", content=CONTENT))


def test_encrypts_as_interoperable_armored_age(notes: FileSystemNotes):
    created = create_private_note(notes)

    encrypted = notes.encrypt(
        created.title,
        NoteSecret(
            passphrase=PASSPHRASE,
            expected_last_modified=created.last_modified,
        ),
    )

    stored = Path(notes._path_from_title(created.title)).read_text()
    assert stored.startswith(AGE_ARMOR_HEADER)
    assert CONTENT not in stored
    assert (
        age_passphrase.decrypt(stored.encode("ascii"), PASSPHRASE).decode()
        == CONTENT
    )
    assert encrypted.encrypted is True
    assert encrypted.content == CONTENT


def test_locked_get_hides_ciphertext_and_unlocks_only_in_memory(
    notes: FileSystemNotes,
):
    created = create_private_note(notes)
    encrypted = notes.encrypt(
        created.title,
        NoteSecret(passphrase=PASSPHRASE),
    )
    ciphertext = Path(notes._path_from_title(created.title)).read_text()

    locked = notes.get(created.title)
    assert locked.encrypted is True
    assert locked.content is None

    unlocked = notes.unlock(
        created.title,
        NoteSecret(
            passphrase=PASSPHRASE,
            expected_last_modified=encrypted.last_modified,
        ),
    )
    assert unlocked.content == CONTENT
    assert (
        Path(notes._path_from_title(created.title)).read_text() == ciphertext
    )


def test_incorrect_passphrase_never_changes_the_file(notes: FileSystemNotes):
    created = create_private_note(notes)
    notes.encrypt(created.title, NoteSecret(passphrase=PASSPHRASE))
    path = Path(notes._path_from_title(created.title))
    ciphertext = path.read_text()

    with pytest.raises(IncorrectPassphraseError):
        notes.unlock(created.title, NoteSecret(passphrase="wrong password"))

    assert path.read_text() == ciphertext


def test_malformed_armored_note_is_rejected(notes: FileSystemNotes):
    created = create_private_note(notes)
    path = Path(notes._path_from_title(created.title))
    malformed = AGE_ARMOR_HEADER + "\nnot-valid-age-data\n"
    path.write_text(malformed)

    with pytest.raises(InvalidEncryptedNoteError):
        notes.unlock(created.title, NoteSecret(passphrase=PASSPHRASE))

    assert path.read_text() == malformed


def test_encrypted_note_indexes_title_but_not_content_or_tags(
    notes: FileSystemNotes,
):
    created = create_private_note(notes)
    notes.encrypt(created.title, NoteSecret(passphrase=PASSPHRASE))

    title_results = notes.search("Private")
    content_results = notes.search("secret")
    tag_results = notes.search("#private-tag")

    assert [result.title for result in title_results] == [created.title]
    assert title_results[0].encrypted is True
    assert content_results == ()
    assert tag_results == ()


def test_saving_unlocked_note_reencrypts_new_content(notes: FileSystemNotes):
    created = create_private_note(notes)
    encrypted = notes.encrypt(created.title, NoteSecret(passphrase=PASSPHRASE))
    updated_content = "New encrypted content"

    updated = notes.update(
        created.title,
        NoteUpdate(
            new_content=updated_content,
            passphrase=PASSPHRASE,
            expected_last_modified=encrypted.last_modified,
        ),
    )

    assert updated.content == updated_content
    assert updated.encrypted is True
    assert (
        notes.unlock(created.title, NoteSecret(passphrase=PASSPHRASE)).content
        == updated_content
    )


def test_stale_client_cannot_overwrite_note(notes: FileSystemNotes):
    created = create_private_note(notes)
    path = Path(notes._path_from_title(created.title))
    path.write_text("Changed elsewhere")

    with pytest.raises(NoteConflictError):
        notes.update(
            created.title,
            NoteUpdate(
                new_content="Stale edit",
                expected_last_modified=created.last_modified,
            ),
        )

    assert path.read_text() == "Changed elsewhere"


def test_permanent_decrypt_restores_plain_markdown(notes: FileSystemNotes):
    created = create_private_note(notes)
    encrypted = notes.encrypt(created.title, NoteSecret(passphrase=PASSPHRASE))

    decrypted = notes.decrypt(
        created.title,
        NoteSecret(
            passphrase=PASSPHRASE,
            expected_last_modified=encrypted.last_modified,
        ),
    )

    assert decrypted.encrypted is False
    assert decrypted.content == CONTENT
    assert Path(notes._path_from_title(created.title)).read_text() == CONTENT
    assert not list(Path(notes.storage_path).glob(".flatnotes-write-*"))
