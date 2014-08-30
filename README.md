DTWT (Do This When That)
-------------------------

A personal IFTTT clone that you can host.

Components
-----------

There is a django app that provides an interface to create channels, triggers,
actions and recipes.

A poller script (under `recipe/poller.py`) that runs every X minutes and checks
for triggers and runs the corresponding actions.

Status
------

Still under development and not stable. More documentation will come as development
stabilizes.

License
-------

MIT License. Please refer the `LICENSE.txt` file.
