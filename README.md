folder_sync
===========

Python package to sync folders.  Especially useful for shared code
in projects with multiple sub projects where using a package manager
seems excessive.

usage:
======

Example project structure
    
    Project
        client/app/jsx/shared_components
    
        admin/app/jsx/shared_components
    
To keep your React components the same between folders setup a file watcher
and when files are saved run the package

Run from the `Project` root.

    folder_sync --target admin/app/jsx/shared_components --target client/app/jsx/shared_components

Then the two folders, and all sub folders, will be kept in sync.

Installation
============

Install directly from the github repo:

    pip install git+git://github.com/Martlark/folder_sync.git#egg=folder_sync

PyCharm
-------

Add as a file watcher, selecting `folder_sync` from the virtual env scripts/bin
directory.  By default `folder_sync` looks for `*.jsx` files.  Change this
with the `--patern` option.  Pick the correct `file type` to match.

When you save any file of `file type` the folders will be synced.

Options
=======

--target folder
---------------

Specify one or more target folders.
Use the option multiple times to allow multiple target folders.

--source folder
---------------

Specify one or more source files to sync into one or more target folders.
Use the option multiple times to allow multiple source folders.  When this
option is not given, `--target` folders are used both as the target and the 
source.

--pattern *.js
--------------

The file pattern to sync.  By default, this is `*.jsx`.

--timed seconds
---------------

Stay running and check for directory synchronization every `--timed` seconds
