NAME

::

    OPD - Original Programmer Daemon


SYNOPSIS

::

    op  <cmd> [key=val] [key==val]
    opc [-i] [-v]
    opd 


DESCRIPTION

::

    OPD has all the python3 code to program a unix cli program, such as
    disk perisistence for configuration files, event handler to
    handle the client/server connection, code to introspect modules
    for commands, deferred exception handling to not crash on an
    error, a parser to parse commandline options and values, etc.

    OPD uses object programming (OP) that allows for easy json save//load
    to/from disk of objects. It provides an "clean namespace" Object class
    that only has dunder methods, so the namespace is not cluttered with
    method names. This makes storing and reading to/from json possible.

    OPD has a demo bot, it can connect to IRC, fetch and display RSS
    feeds, take todo notes, keep a shopping list and log text. You can
    also copy/paste the service file and run it under systemd for 24/7
    presence in a IRC channel.

    OPD is Public Domain.


INSTALL

::

    $ pipx install opd
    $ pipx ensurepath

    <new terminal>

    $ op srv > opd.service
    # mv *.service /etc/systemd/system/
    # systemctl enable opd --now

    joins #op on localhost


USAGE

::

    without any argument the bot does nothing::

    $ op
    $

    see list of commands

    $ op cmd
    cmd,skl,srv


    start a console

    $ opc
    >

    start daemon

    $ opd
    $ 


CONFIGURATION

::

    irc

    $ op cfg server=<server>
    $ op cfg channel=<channel>
    $ op cfg nick=<nick>

    sasl

    $ op pwd <nsvnick> <nspass>
    $ op cfg password=<frompwd>

    rss

    $ op rss <url>
    $ op dpl <url> <item1,item2>
    $ op rem <url>
    $ op nme <url> <name>


COMMANDS

::

    cfg - irc configuration
    cmd - commands
    mre - displays cached output
    pwd - sasl nickserv name/pass


FILES

::

    ~/.op
    ~/.local/bin/op
    ~/.local/bin/opc
    ~/.local/bin/opd
    ~/.local/pipx/venvs/opd/*


AUTHOR

::

    Bart Thate <bthate@dds.nl>


COPYRIGHT

::

    OPD is Public Domain.
