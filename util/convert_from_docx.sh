#!/bin/sh
# Converts Will's docx to txt 
# Ondrej Chvala
# MIT license

for f in $(ls -1 *docx); do echo $f; docx2txt $f ;done
for f in $(ls -1 *txt); do echo $f; sed -i '/---------------------$/d'  $f ;done
sed -i s/#-------------------------------#//g *txt

