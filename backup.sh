#!/bin/sh
./manage.py dumpdata --indent=4 sites main mechanic webtheme> apps/main/fixtures/initial.json 


