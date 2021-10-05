py_sync
=======

Python package to sync folders and files.  Especially useful for shared code
in projects with multiple sub projects where using a package manager
seems excessive.

usage:
======

Example project structure
    
    Project
        client/app/jsx/shared_components
    
        admin/app/jsx/shared_components
    
To keep your React components the same between folders setup a file watcher
and when files are saved run `py_sync`.

Run from the `Project` root.

    py_sync --target admin/app/jsx/shared_components --target client/app/jsx/shared_components  --patttern '**/*.jsx'

Then the two folders, and all sub folders, will be kept in sync.

Installation
============

Install directly from the github repo:

    pip install git+git://github.com/Martlark/py_sync.git#egg=py_sync

PyCharm
-------

Add as a file watcher, selecting `py_sync` from the virtual env scripts/bin
directory.  By default `py_sync` looks for `*` all files.  Change this
with the `--patern` option.  Pick the correct `file type` to match.  For the
above folder structure use:

    py_sync --target admin/app/jsx/shared_components --target client/app/jsx/shared_components

When you save any file of `file type` the folders will be synced.

Options
=======

--target folder
---------------

Specify one or more target folders.
Use the option multiple times to allow multiple target folders.

NOTE: the top level target folder must exist.  Lower level folder 
structures will be created during synchronization.

--source folder
---------------

Specify one or more source files to sync into one or more target folders.
Use the option multiple times to allow multiple source folders.  When this
option is not given, `--target` folders are used both as the target and the 
source.

--pattern **/*
--------------

The file pattern to sync.  By default, this is all files, ie: `**/*`.

NOTE: `**/` will be prepended to any pattern if it is not found at the start. That
means all synchronization is recursive for folders.

NOTE: surround this option value with single quotes (in unix) to prevent
shell expansion.

--syncfiles file1,file2,file3,....
----------------------------------

Specify a comma separated list of files to keep the same.  Files and
folders will be created as required.  Files are checked from file1 onwards
and then checked in the reverse direction.

NOTE: `--pattern` option is not used with `--syncfiles`

--timed seconds
---------------

Stay running and check for directory synchronization every `--timed` seconds
