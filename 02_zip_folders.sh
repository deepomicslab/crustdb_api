#!/usr/bin/bash

src_path="/home/platform/project/crustdb_platform/crustdb_api/workspace/crustdb_database/Axolotls/"
des_path="/home/platform/project/crustdb_platform/crustdb_api/workspace/crustdb_database/Zipped_Axolotls/"

cd $src_path

files=$(ls -l $src_path | awk '{print $9}')

for file in $files
do
    # echo $file
    cd ./${file}
    zip -q ./${file}.zip ./*
    mv ./${file}.zip ${des_path}/
    cd ..
    # break
done