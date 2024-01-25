import os
import subprocess


def ping_ip(ip):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    # Building the command. Ex: "ping -c 1 google.com"
    command = ["ping", "-c 1", ip]

    with open(os.devnull, "w") as devnull:
        res_command = subprocess.call(command, stdout=devnull, stderr=devnull) == 0
    return res_command
