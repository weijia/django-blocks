#!/bin/bash

PROJECT_HOME=$(cd $(dirname $0)/.. && pwd)

cd $PROJECT_HOME/personal

./manage.py $@
