Python package to sync folders.

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

Options
=======

--source 
--------

Specify one or more source files to sync into one or more target folders

--pattern
---------

The file pattern to sync.  By default, this is `*.jsx`.
