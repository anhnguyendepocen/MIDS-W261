#!/bin/bash
set -x -e

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
pip install requests numpy
pip install matplotlib
#pip install scipy
#pip install scikit-learn

#Create profile 	
jupyter notebook --generate-config

#Run on master /slave based on configuration

echo "c = get_config()" >  /home/hadoop/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.ip = '*'" >>  /home/hadoop/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.open_browser = False"  >>  /home/hadoop/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.port = 8192" >>  /home/hadoop/.jupyter/jupyter_notebook_config.py
nohup jupyter notebook --no-browser > /mnt/var/log/jupyter_notebook.log &
