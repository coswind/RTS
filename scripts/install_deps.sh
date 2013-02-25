#!/bin/bash

# dependency scrapyd-0.12/scrapy-0.12 does not install here for it daemon process issues and need install in projects import it.
SYS_DEPS=(python-pip s3cmd python-mysqldb automake libtool libmysqlclient15-dev libxml2-dev libexpat1-dev m4 autoconf automake libtool)

PYTHON_DEPS=( django setproctitle pymysql pika )

function install_dependencies()
{
    # update to latest to avoid some packages can not found.
    aptitude update
    echo "Installing required system packages..."
    for sys_dep in ${SYS_DEPS[@]};do
       install_sys_dep $sys_dep
    done
    echo "Installing required system packages finished."

    echo "Installing required python packages..."
    for python_dep in ${PYTHON_DEPS[@]};do
       install_python_dep ${python_dep}
    done
    echo "Installing required python packages finished."

}

function install_sys_dep()
{
    # input args  $1 package name
    if [ `aptitude  search  $1  | grep -c "^i \+${1} \+"` = 0 ];then
        aptitude -y install  $1
    else
        echo "Package ${1} already installed."
    fi
}

function install_python_dep()
{
    # input args $1 like simplejson==1.0 ,can only extractly match
    if [ `pip freeze | grep -c "${1}"` = 0 ];then
        pip install  $1
    else
        echo "Python package ${1} already installed."
    fi
}

function install_coreseek()
{
    # download coreseek
    cd /tmp
    wget http://www.coreseek.cn/uploads/csft/4.0/coreseek-4.1-beta.tar.gz
    tar xzvf coreseek-4.1-beta.tar.gz
    cd coreseek-4.1-beta

    # install mmseg
    cd mmseg-3.2.14
    ./bootstrap
    ./configure --prefix=/usr/local/mmseg3
    make && make install
    cd ..

    # install coreseek
    cd csft-4.1
    sh buildconf.sh
    ./configure --prefix=/usr/local/coreseek  --without-unixodbc --with-mmseg --with-mmseg-includes=/usr/local/mmseg3/include/mmseg/ --with-mmseg-libs=/usr/local/mmseg3/lib/ --with-mysql --enable-id64
    make && make install
    cd ..

    # test mmseg
    cd testpack
    cat var/test/test.xml
    /usr/local/coreseek/bin/indexer -c etc/csft.conf --all
    /usr/local/coreseek/bin/search -c etc/csft.conf 网络搜索
}

install_dependencies
install_coreseek

# create database fakemusic
# grant all on fakemusic.* to music@"%" identified by "P@55word"
