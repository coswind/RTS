#!/bin/bash
#
# create database fakemusic
# grant all on fakemusic.* to music@"%" identified by "P@55word"

SCRIPT_DIR=`dirname $0`

PASSWORD=P@55word

DATABASE=fakemusic

function setupDB()
{
    mysql -u root -p$PASSWORD -e "create database $DATABASE"
    mysql -u root -p$PASSWORD -e "grant all on $DATABASE.* to music@'%' identified by 'P@55word'"
    mysql -u root -p$PASSWORD $DATABASE < $SCRIPT_DIR/sph_counter.sql
}

setupDB
