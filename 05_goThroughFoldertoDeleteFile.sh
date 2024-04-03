#!/usr/bin/bash

path="/home/platform/project/crustdb_platform/crustdb_api/workspace/crustdb_database/Axolotls/"
cd $path

files=$(ls -l $path | awk '{print $9}')

for file in $files
do
    # echo $file
    cd ./${file}
    rm ./*.png
    echo $file
    cd ..
    # break
done