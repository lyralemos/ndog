# NDOG

## The ngix watchdog

This script watch for create and delete events inside a folder. 
For each .conf file created, it creates a symlink in the destination folder.
Everytime a file is deleted, it removes the symlink.

It also reloads nginx for both events.

### Prerequisites

This script depends on the [watchdog](https://pypi.org/project/watchdog/) library.

### Usage

```
ndog /src/folder /dest/folder
```

ndog will listen to events in the **/src/folder** and creates symlinks in **/dest/folder**.