# utilities for perforce

import contextlib
import datetime
import getpass
import json
import os
import os.path
import socket
import subprocess

import click

from . import tools, winget
from .tools import locations

# path prefix for p4 command
p4_prefix = None

# fingerprints for various p4 servers


def p4_run(args, parse=False, **kwargs):
    """run a p4 command, and return the output"""
    # We have logic here to be able to find p4 even if we just installed it and
    # it is not in the PATH
    global p4_prefix
    if p4_prefix:
        p4 = os.path.join(p4_prefix, "p4.exe")
    else:
        p4 = "p4"

    # inherit and override environment variables
    if "env" in kwargs:
        kwargs["env"] = dict(os.environ, **kwargs["env"])

    # add options for json output
    options = []
    if parse:
        options += ["-ztag", "-Mj"]
        kwargs["capture_output"] = True
        kwargs["check"] = True

    cmd = [p4] + options + args
    try:
        # print(f"running {cmd} with {kwargs}")
        out = subprocess.run(cmd, **kwargs)
    except FileNotFoundError:
        if p4_prefix:
            raise
        p4_prefix = os.path.join(os.environ["ProgramFiles"], "Perforce")
        p4 = os.path.join(p4_prefix, "p4.exe")
        cmd = [p4] + options + args
        out = subprocess.run(cmd, **kwargs)

    if parse:
        return json.loads(out.stdout.decode())
    return out


location_type = click.Choice(locations.keys(), case_sensitive=False)


def validate_work_drive(cxt, param, drive: str):
    if len(drive) == 1:
        drive = drive + ":"
    if len(drive) != 2 or drive[1] != ":" or not drive[0].isalpha():
        raise click.BadParameter(
            "work drive must be a single letter followed by a colon"
        )
    if drive.upper() == "P:" or not os.path.isdir(drive):
        raise click.BadParameter(f"{drive} is not a valid drive")
    return drive.upper()


@click.group()
def p4():
    pass


@p4.command()
@click.option("--force", is_flag=True, help="force install")
@click.option(
    "--location", type=location_type, prompt="Specify your location", required=True
)
@click.option(
    "--work-drive",
    type=str,
    required=True,
    prompt="Specify your work drive (e.g. D:)",
    callback=validate_work_drive,
)
@click.option("--sync/--no-sync", default=True, help="sync after setup")
def initial_setup(force, location, work_drive, sync):
    """Inintial setup of p4 for PaxDei development"""
    do_initial_setup(force, location, work_drive, sync=sync)


def do_initial_setup(force, location, work_drive, sync=False):
    """Inintial setup of p4 for PaxDei development"""
    print("welcome to initial_setup_p4")

    # optionally install p4
    version = have_p4()
    if not version or force:
        do_install(force)
        version = have_p4()
    print(f"p4 version {version}")

    # various settings
    p4_set_various()

    # set p4port and p4trust
    tools.location_set(location)
    set_location(location)

    # set the client to the paxdei depot by default
    p4client_set(get_client_name("paxdei"))

    # login
    do_login(quiet=True)

    # create the client specs
    tools.workdrive_set(work_drive)
    for depot in ["paxdei", "UE"]:
        do_create_client(work_drive, depot)

    # create the subst
    do_subst_drive(work_drive, force=True)

    # sync
    if sync:
        print("syncing depots")
        do_sync(all=True)
    print("done")


@p4.command()
@click.option("-f", "--force", is_flag=True, help="force install")
def install(force):
    """install p4"""
    do_install(force)


def do_install(force):
    version = have_p4()
    if version:
        print(f"current p4 version {version}")
    else:
        print("p4 not found")
    pass
    winget.install("Perforce.P4V")


@p4.command()
def version():
    version = have_p4()
    if version:
        print(f"p4 version {version}")
    else:
        print("p4 not found")


@p4.command()
@click.option("--quiet/--no-quiet", default=False)
def login(quiet=False):
    return do_login(quiet)


def do_login(quiet=False):
    out = p4_run(["login", "-s"], capture_output=True)
    if out.returncode == 0:
        if not quiet:
            print("Already logged in. " + out.stdout.decode().strip())
        return True
    print(
        "not logged in.  please login, and look for a JumpCloud notification on your phone."
    )
    out = p4_run(["login"])
    return out.returncode == 0


def set_location(location):
    p4port = get_p4port(location)
    print(f"setting P4PORT to {p4port}")
    p4_run(["set", f"P4PORT={p4port}"], check=True)
    p4trust = get_p4trust(location)
    p4_run(["trust", "-f", "-i", p4trust], check=True)


def get_p4port(location):
    """return a suitable value for P4PORT"""
    return locations[location]["p4port"]


def get_p4trust(location):
    """return a suitable value for P4TRUST"""
    loc = locations[location]
    return loc["p4trust"]


def have_p4():
    version = None
    try:
        output = p4_run(["-V"], capture_output=True, check=True)
        for line in output.stdout.decode().split("\n"):
            if line.startswith("Rev."):
                version = line.split()[1].split("/")[2]
                break
    except subprocess.CalledProcessError:
        pass

    return version


def p4_set_various():
    """Set various p4 options"""
    p4_run(["set", "P4CHARSET=utf8"])
    p4_run(["set", "P4COMMANDCHARSET=utf8"])
    p4_run(["set", "P4CONFIG=.p4config"])
    p4_run(["set", "P4IGNORE=p4ignore.txt;.p4ignore"])


@p4.command()
@click.option(
    "--workdrive",
    type=str,
    prompt="Specify the workdrive",
    callback=validate_work_drive,
)
@click.option("--depot", type=str, prompt="Specify the depot")
def create_client(workdrive, depot):
    """create a new client for the given depot"""

    do_create_client(workdrive, depot)


def do_create_client(workdrive, depot, stream="main"):
    client_name = get_client_name(depot)
    client_root = os.path.join(workdrive, "p4", depot)
    date = datetime.datetime.now(tz=datetime.UTC).strftime("%Y/%m/%d %H:%M:%S %Z")
    client_spec = f"""
Client: {client_name}
Owner: {get_username()}
Host: {get_hostname()}
Description:
 Created by paxo on {date}
Root: {client_root}
Options: rmdir
Stream: //{depot}/{stream}
View:
 //{depot}/{stream}/... //{client_name}/...
"""
    p4_run(["client", "-i"], input=client_spec.encode(), check=True)
    os.makedirs(client_root, exist_ok=True)
    write_p4config(client_name, client_root)
    return client_name


def write_p4config(client_name, client_root):
    p4config = f"""
P4CLIENT={client_name}
"""
    with open(os.path.join(client_root, ".p4config"), "w") as f:
        f.write(p4config)


def get_client_name(depot, postfix=None):
    """return a suitable client name for the given stream"""
    name = f"pd_{get_username()}_{get_hostname()}_{depot}"
    if postfix:
        name += f"_{postfix}"
    return name


def get_hostname():
    return socket.gethostname()


def get_username():
    return getpass.getuser()


def p4client_set(client):
    """set the current client"""
    p4_run(["set", f"P4CLIENT={client}"], check=True)


def p4client_get():
    """get the current client"""
    out = p4_run(["set", "P4CLIENT"], check=True, capture_output=True)
    return out.stdout.decode().strip().split("=")[1].split()[0]


@contextlib.contextmanager
def p4client(client):
    """context manager for setting the current client"""
    old_client = p4client_get()
    p4client_set(client)
    try:
        yield
    finally:
        p4client_set(old_client)


@p4.command()
@click.option("--depot", type=str, prompt="Specify the depot", default="paxdei")
@click.option("--all", is_flag=True, help="sync all depots")
def sync(depot):
    """sync the given depot"""
    do_sync(depot)


def do_sync(depot="paxdei", all=False):
    if all:
        depots = ["paxdei", "UE"]
    else:
        depots = [depot]
    for d in depots:
        client = get_client_name(depot=d)
        with p4client(client):
            p4_run(["sync"], check=True)


@p4.command()
@click.option("--depot", type=str, default="paxdei")
@click.argument("stream-name")
def switch(depot, stream_name):
    """switch to the given stream"""
    client = get_client_name(depot)
    res = p4_run(["switch", stream_name], check=False, env={"P4CLIENT": client})
    return res.returncode != 0


@p4.command()
@click.option("--depot", type=str, default="paxdei")
def get_stream(depot):
    """get the current stream"""
    client = get_client_name(depot)
    out = p4_run(["switch"], check=True, capture_output=True, env={"P4CLIENT": client})
    stream = out.stdout.decode().strip()
    print(f"client {client} is on stream '{stream}'")


@p4.command()
@click.option("--work-drive", type=str, default=None)
@click.option("--force", is_flag=True, help="force resubst")
def subst(work_drive, force):
    ok = do_subst_drive(work_drive, force)
    if not ok:
        print("substitution failed, already exists.  use --force to override")


def do_subst_drive(work_drive=None, force=False):
    """Subst the paxdei root folder to the P: drive"""
    # P will have the structure
    # P:\paxdei
    # P:\UE
    # P:\otherstuff

    if not work_drive:
        client = get_client_name(depot="paxdei")
        print(f"client is {client}")
        client_info = get_client_info(client)
        client_root = client_info["Root"]
        work_drive = os.path.splitdrive(client_root)[0]

    if len(work_drive) == 1:
        work_drive = work_drive + ":"

    src = os.path.join(work_drive, "\p4")
    dst = "P:"

    out = subprocess.run(["subst", dst, src], capture_output=True)
    if out.returncode == 0:
        return True

    if "already" not in out.stdout.decode():
        out.check_returncode()

    if force:
        subprocess.run(["subst", dst, "/d"], check=True)
        subprocess.run(["subst", dst, src], check=True)
        return True
    return False


def get_client_info(client):
    """return the client info for the given client"""
    out = p4_run(["client", "-o", client], parse=True)
    return out


def fix_p4v_settings():
    # fix the p4v xml settings file
    filename = os.path.join(
        os.environ["USERPROFILE"], ".p4qt", "ApplicationSettings.xml"
    )
    import xml.etree.ElementTree as ElementTree

    tree = ElementTree.parse(filename)
    root = tree.getroot()
    for elem in root.iter():
        print(elem)
