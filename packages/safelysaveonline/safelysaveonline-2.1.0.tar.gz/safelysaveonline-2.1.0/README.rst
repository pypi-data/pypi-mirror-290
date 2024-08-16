SafelySaveOnline
===================================

SafelySaveOnline is a python libary making it easy to save encrypted dictionaries and store them in a git repository.

Installing
----------

You can install SafelySaveOnline with:

::

   pip install safelysaveonline

Usage
-----

Import SafelySaveOnline with:

::

   import safelysave

You can create a profile with: You can find the profile under safelysaveonline
in your appdata directory.

::

   safelysave.create_profile(git_repo_address)

Now add a dictionary with:

::

   safelysave.add_dict(profile_uuid, dictionary)

Push it to your repo with:

::

   safelysave.sync(profile_uuid)

You can find out more at https://codeberg.org/VisualXYW/safelysaveonline/wiki
(WIP).
