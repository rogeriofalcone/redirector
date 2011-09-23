#!/bin/sh
./manage.py dumpdata --indent=4 sites main mechanic webtheme menu_manager> apps/main/fixtures/initial.json 


