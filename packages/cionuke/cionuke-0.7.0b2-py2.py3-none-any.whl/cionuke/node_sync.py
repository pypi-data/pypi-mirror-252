'''
This script synchronizes instances within a single CopyCat job to allow for distributed workloads.

CopyCat (i.e.: PyTorch) requires one worker to be the primary worker. All other workers connect
to the primary worker. The primary worker is responsible for writing out all the files.

We take advantage that on CoreWeave, all the tasks within a job use shared storage for the output
path.

The first task to start running creates a .lock file in the output path that contains its IP.

As other tasks spin-up, if they see the .lock file, they read the IP and then use it to connect to the
primary worker.
'''

import logging
import os
import os.path
import stat
import subprocess
import sys

print("Running worker sync script...")

ROOT_PATH = os.path.dirname(__file__)
LOCK_FILE = os.path.join(ROOT_PATH, ".lock")

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

primary_node_ip = None
is_primary_node = False

def get_ip_address():
    ip_address = os.environ['AGENT_DNS_RECORD']
    logger.info("Found IP of instance: {}".format(ip_address))
    return ip_address

logger.debug("Contents of {}".format(ROOT_PATH))
for i in os.listdir(ROOT_PATH):
    logger.debug(i)


if os.path.exists(LOCK_FILE):
    
    logger.info("Lock file ({}) exists. Reading IP address of primary render node".format(LOCK_FILE))
    
    with open(LOCK_FILE, 'r') as fh:
        data = fh.readlines()
        logger.debug("Contents of lock file:\n{}".format(data))
    
    primary_node_ip = data[0]    
    logger.info("Using %s as IP address of primary render instance", primary_node_ip)

else:
    logger.info("Lock file (%s) doesn't exist. Writing IP into lock file.", LOCK_FILE)
    
    primary_node_ip = get_ip_address()
    is_primary_node = True
    
    with open(LOCK_FILE, 'a') as fh:
        fh.write("{}\n".format(get_ip_address()))

if is_primary_node:
    copycat_rank = "0"

else:
    copycat_rank = "1"

if not os.environ['CONDUCTOR_OUTPUT_PATH'].startswith("/"):
    output_path = os.environ['CONDUCTOR_OUTPUT_PATH'][2:]

else:
    output_path = os.environ['CONDUCTOR_OUTPUT_PATH']

cmd_script = "{}.sh".format(os.path.join(output_path, get_ip_address()))

cmd_script_contents = []

with open(cmd_script, 'w') as fh:
    cmd_script_contents.append("#!/usr/bin/env bash\n")    
    cmd_script_contents.append("export COPYCAT_MAIN_PORT=60000\n")
    cmd_script_contents.append("export COPYCAT_RANK={}\n".format(copycat_rank))
    cmd_script_contents.append("export COPYCAT_WORLD_SIZE=2\n")

    if is_primary_node:
        cmd_script_contents.append("export COPYCAT_MAIN_ADDR=0.0.0.0\n")

    else:
        cmd_script_contents.append("export COPYCAT_MAIN_ADDR={}\n".format(primary_node_ip))

    cmd_script_contents.append("nuke -F 1 -X {} --multigpu --gpu {}\n".format(sys.argv[1], " ".join(sys.argv[2:])))
    fh.writelines(cmd_script_contents)

os.chmod(cmd_script, stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR)

os.environ['COPYCAT_MAIN_PORT'] = "60000"
os.environ['COPYCAT_RANK'] = copycat_rank
os.environ['COPYCAT_MAIN_ADDR'] = primary_node_ip
os.environ['COPYCAT_WORLD_SIZE'] = "2"

cmd_script = ["nuke", "-F", "1", "-X", sys.argv[1], "--multigpu", "--gpu", sys.argv[2]]

print("Starting Nuke: {}".format(" ".join(cmd_script)))
p = subprocess.run(cmd_script, check=False, shell=False)
print("Process completed. Return code: {}".format(p.returncode))
