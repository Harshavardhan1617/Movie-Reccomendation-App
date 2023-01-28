#!/bin/bash
PATH=/home/harsha/anaconda3/envs/twint-env/bin:/home/harsha/anaconda3/condabin:/home/harsha/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin
source /home/harsha/anaconda3/etc/profile.d/conda.sh
# Uncomment this line to include .profile for environment variables
# source ~/.profile

conda activate twint-env
python "$@"
