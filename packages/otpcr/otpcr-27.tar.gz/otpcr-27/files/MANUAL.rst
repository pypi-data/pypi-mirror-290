README
######


**NAME**

::

   OTPCR - Elderly, Handicapped, Criminals, Wicked


**SYNOPSIS**

::

    otpcr <cmd> [key=val] [key==val]
    otpcrc [-a] [-i] [-v]
    otpcrd


**DESCRIPTION**


``OTPCR`` holds evidence that king netherlands
is doing a genocide, a written response
where king netherlands confirmed taking note
of “what i have written”, namely proof that
medicine he uses in treatement laws like
zyprexa, haldol, abilify and clozapine are
poison that make impotent, is both physical
(contracted muscles) and mental (make people
hallucinate) torture and kills members of the
victim groups.

``OTPCR`` contains correspondence with the
International Criminal Court, asking for the
arrest of king netherlands, for the genocide
he is committing with his new treatement laws.

Current status is a "no basis to proceed"
judgement of the prosecutor which requires
a "basis to prosecute" to have the king
actually arrested and, thereby, his genocide
stopped.


INSTALL

::

    $ pipx install otpcr
    $ pipx ensurepath

    <new terminal>

    $ nixt srv > otpcr.service
    $ sudo mv otpcr.service /etc/systemd/system/
    $ sduo systemctl enable otpcr --now

    joins #otpcr on localhost


**USAGE**

without any argument the bot does nothing::

    $ otpcr
    $

see list of commands::

    $ otpcr cmd
    cmd,dne,err,log,mod,req,tdo,thr,tmr

start a console::

    $ otpcrc
    >


use -i to run init on modules::

    $ otpcrc -ai

start daemon::

    $ otpcrd

show request to the prosecutor::

    $ otpcr req
    Information and Evidence Unit
    Office of the Prosecutor
    Post Office Box 19519
    2500 CM The Hague
    The Netherlands


**CONFIGURATION**

irc::

    $ otpcr cfg server=<server>
    $ otpcr cfg channel=<channel>
    $ otpcr cfg nick=<nick>

sasl::

    $ otpcr pwd <nsvnick> <nspass>
    $ otpcr cfg password=<frompwd>

rss::

    $ otpcr rss <url>
    $ otpcr dpl <url> <item1,item2>
    $ otpcr rem <url>
    $ otpcr nme <url> <name>

opml::

    $ otpcr imp <filename>
    $ otpcr exp


**OPTIONS**

here is a list of commandline options ``otpcr`` provides::

    -a     load all modules
    -i     start services
    -v     use verbose


**COMMANDS**

commands are mostely for irc and rss management::

    cfg - irc configuration
    cmd - commands
    dlt - remove a user
    dpl - sets display items
    exp - export opml
    fnd - find objects 
    imp - import opml
    log - log some text
    met - add a user
    mre - displays cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    req - request 
    rss - add a feed
    thr - show the running threads


**FILES**

pipx stores the ``otpcr`` documentation in it;s local pipx environment::

    ~/.otpcr
    ~/.local/bin/otpcr
    ~/.local/bin/otpcrc
    ~/.local/bin/otpcrd
    ~/.local/pipx/venvs/otpcr/*


**AUTHOR**

I am reachable at the following email::

    Bart Thate <bthate@dds.nl>


**COPYRIGHT**

::

    OTPCR is placed in the Public Domain.
