#!/bin/bash

SCRIPT_DIR=`dirname $0`

USER=xxxxxx

PROJECT=music-importer

PROJECT_DIR="/var/app/enabled/$PROJECT"

[ -z `grep "^$USER:" /etc/passwd` ] && sudo useradd -r $USER -M -N

chown -R $USER:nogroup /var/app/enabled/$PROJECT
chown -R $USER:nogroup /var/app/data/$PROJECT
chown -R $USER:nogroup /var/app/log/$PROJECT

chmod -R a+rw /var/app/data/$PROJECT
chmod -R a+rw /var/app/log/$PROJECT

if [ "$1" = "checkdeps" ] ; then
    if [ -f "${SCRIPT_DIR}/install_deps.sh" ]; then
        ${SCRIPT_DIR}/install_deps.sh
    fi
fi
