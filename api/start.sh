#!/bin/bash

./db_init/init_db.sh &
python -u app.py