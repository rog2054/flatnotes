<p align="center">
  <img src="docs/logo.svg" width="300px"></img>
</p>
<p align="center">
  <img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/dullage/flatnotes?style=for-the-badge">
</p>

A self-hosted, database-less note-taking web app that utilises a flat folder of markdown files for storage.

---
**FORK**
This fork adds optional, passphrase-protected note encryption using the
standard [age](https://age-encryption.org/) file format. Ordinary notes remain
normal Markdown files, while encrypted notes remain independently recoverable
with age-compatible tools.
 ---

## Contents

- [Design Principle](#design-principle)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Hosted](#hosted)
  - [Self Hosted](#self-hosted)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Sponsorship](#sponsorship)
- [Thanks](#thanks)

## Design Principle

flatnotes is designed to be a distraction-free note-taking app that puts your note content first. This means:

- A clean and simple user interface.
- No folders, notebooks or anything like that. Just all of your notes, backed by powerful search and tagging functionality.
- Quick access to a full-text search from anywhere in the app (keyboard shortcut "/").

Another key design principle is not to take your notes hostage. Your notes are just markdown files. There's no database, proprietary formatting, complicated folder structures or anything like that. You're free at any point to just move the files elsewhere and use another app.

Equally, the only thing flatnotes caches is the search index and that's incrementally synced on every search (and when flatnotes first starts). This means that you're free to add, edit & delete the markdown files outside of flatnotes even whilst flatnotes is running.

## Features

- Mobile responsive web interface.
- Raw/WYSIWYG markdown editor modes.
- Advanced search functionality.
- Note "tagging" functionality.
- Customisable home page.
- Wikilink support to easily link to other notes (`[[My Other Note]]`).
- Light/dark themes.
- Multiple authentication options (none, read-only, username/password, 2FA).
- Restful API.
- Optional age-encrypted note contents with in-browser session unlocking.

## Encrypted Notes

Open an existing note and select **Encrypt** to replace its Markdown contents
with an ASCII-armoured, passphrase-encrypted age payload. The passphrase is
kept only in the current browser tab's memory and is sent over the authenticated
connection when an encrypted note is unlocked or saved. It is never written to
Flatnotes configuration, browser storage, cookies, or the note directory.

Encrypted notes can be locked again, edited and re-encrypted, or permanently
decrypted from the note screen. Writes use an atomic file replacement and are
rejected if the note changed after it was loaded.

### Security Boundary

Encryption protects note contents in the data directory and its backups. It is
server-side encryption: the running Flatnotes server receives the passphrase
and sees plaintext while servicing an unlocked note, so use HTTPS and operate
the server as a trusted system.

The following remain plaintext and may reveal sensitive metadata:

- Note titles and filenames.
- Note count, sizes, and modification times.
- Files in the `attachments` directory, including attachments linked from an
  encrypted note.
- The title and modification time stored in the Whoosh search index.

Encrypted note contents and tags are not added to the search index. Encrypted
notes can still be found by their plaintext title and appear in recent/all-note
lists with a lock indicator. Browser drafts are deliberately disabled for
encrypted notes so plaintext is not persisted in web storage.

There is no password reset or recovery mechanism. Losing a passphrase means
losing access to the corresponding note.

### Recovery Outside Flatnotes

Encrypted notes remain `.md` files containing standard ASCII-armoured age
data. To recover one independently, install the official age command and run:

```shell
age --decrypt "My Encrypted Note.md" > "My Encrypted Note.decrypted.md"
```

Enter the note's passphrase when prompted. Keep backups of encrypted files
before performing bulk or external operations.

See [the wiki](https://github.com/dullage/flatnotes/wiki) for more details.

## Getting Started

### Hosted

A quick and easy way to get started with flatnotes is to host it on PikaPods. Just click the button below and follow the instructions.

[![PikaPods](https://www.pikapods.com/static/run-button-34.svg)](https://www.pikapods.com/pods?run=flatnotes)

### Self Hosted

If you'd prefer to host flatnotes yourself then the recommendation is to use Docker.

### Example Docker Run Command

```shell
docker run -d \
  -e "PUID=1000" \
  -e "PGID=1000" \
  -e "FLATNOTES_AUTH_TYPE=password" \
  -e "FLATNOTES_USERNAME=user" \
  -e 'FLATNOTES_PASSWORD=changeMe!' \
  -e "FLATNOTES_SECRET_KEY=aLongRandomSeriesOfCharacters" \
  -v "$(pwd)/data:/data" \
  -p "8080:8080" \
  dullage/flatnotes:latest
```

### Example Docker Compose

```yaml
version: "3"

services:
  flatnotes:
    container_name: flatnotes
    image: dullage/flatnotes:latest
    environment:
      PUID: 1000
      PGID: 1000
      FLATNOTES_AUTH_TYPE: "password"
      FLATNOTES_USERNAME: "user"
      FLATNOTES_PASSWORD: "changeMe!"
      FLATNOTES_SECRET_KEY: "aLongRandomSeriesOfCharacters"
    volumes:
      - "./data:/data"
      # Optional. Allows you to save the search index in a different location:
      # - "./index:/data/.flatnotes"
    ports:
      - "8080:8080"
    restart: unless-stopped
```

See the [Environment Variables](https://github.com/dullage/flatnotes/wiki/Environment-Variables) article in the wiki for a full list of configuration options.

## Roadmap

I want to keep flatnotes as simple and distraction-free as possible which means limiting new features. This said, I welcome feedback and suggestions.

## Contributing

If you're interested in contributing to flatnotes, then please read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Sponsorship

If you find this project useful, please consider buying me a beer. It would genuinely make my day.

[![Sponsor](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/Dullage)

## Thanks

A special thanks to 2 fantastic open-source projects that make flatnotes possible.

- [Whoosh](https://whoosh.readthedocs.io/en/latest/intro.html) - A fast, pure Python search engine library.
- [TOAST UI Editor](https://ui.toast.com/tui-editor) - A GFM Markdown and WYSIWYG editor for the browser.
