import subprocess

# stuff to install with winget


def install(id, force=False):
    cmd = ["winget", "install", "-e", "--id", id]
    subprocess.run(cmd)
