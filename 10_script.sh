#!/bin/bash

trap "echo; echo 'script end'; exit" SIGINT
echo "if want end ,Ctrl + C"

module load GCCcore/11.2.0 GCC/11.2.0 Python/3.9.6

while true
do
    /apps/software/Python/3.9.6-GCCcore-11.2.0/bin/python /home/platform/project/crustdb_platform/crustdb_api/manage.py crontab run a19514c2b24eaf87de6a6c500a7ff3a3
    echo run contab
    sleep 1m
done