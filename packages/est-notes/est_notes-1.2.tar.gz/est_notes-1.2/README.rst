Encrypted, synchronised todos (WIP)
===================================

EST (Encrypted, synchronised todos) is a python libary making it easy to
create an encrypted, git-synced todo/notes application.

! EST is an hobby project, issues are exspected. Use at your own risk!

Installing
----------

You can install EST with:

::

   pip install est-notes

Usage
-----

Import EST with:

::

   import est_notes

You can create a profile with: You can find the profile under est-notes
in your appdata directory.

::

   est_notes.create_profile(git_repo_address, '')

Now add a todo/note with:

::

   est_notes.create_profile(profile_uuid, content)

Push it to your repo with:

::

   est_notes.sync(profile_uuid)

You can find out more at https://codeberg.org/VisualXYW/est-notes/wiki
(WIP).
