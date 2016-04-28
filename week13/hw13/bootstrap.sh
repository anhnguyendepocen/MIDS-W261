#!/bin/bash
set -x -e

# Determine if we are running on the master node.
# 0 - running on master
# 1 - running on a task or core node
check_if_master() {
    python - <<'__SCRIPT__'
import sys
import json
 
instance_file = "/mnt/var/lib/info/instance.json"
is_master = False
try:
    with open(instance_file) as f:
        props = json.load(f)
 
    is_master = props.get('isMaster', False)
    print props
except IOError as ex:
    pass # file will not exist when testing on a non-emr machine
 
if is_master:
    sys.exit(0)
else:
    sys.exit(1)
__SCRIPT__
}

check_if_master
if [ 1 -eq 0 ]
then
	# upgrade packages
	sudo yum upgrade -y
	sudo pip install --upgrade pip

	#Installing Jupyter Notebook
	cd /home/hadoop

	mkdir jupyter
	cd jupyter
	virtualenv venv
	source venv/bin/activate

	#Install ipython and dependency
	pip install "jupyter"
	pip install matplotlib

	#Create profile 	
	jupyter notebook --generate-config

	#Run on master /slave based on configuration

	echo "c = get_config()" >  /home/hadoop/.jupyter/jupyter_notebook_config.py
	echo "c.NotebookApp.ip = '*'" >>  /home/hadoop/.jupyter/jupyter_notebook_config.py
	echo "c.NotebookApp.open_browser = False"  >>  /home/hadoop/.jupyter/jupyter_notebook_config.py
	echo "c.NotebookApp.port = 8192" >>  /home/hadoop/.jupyter/jupyter_notebook_config.py
	nohup jupyter notebook --no-browser > /mnt/var/log/jupyter_notebook.log &
else
	echo "Not a master node, skipping"
fi
exit 0