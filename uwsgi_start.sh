#!/bin/bash

#uwsgi --socket :8001 --module config.wsgi
uwsgi --socket /tmp/projectname.stats.sock --socket 127.0.0.1:8001 --module config.wsgi --stats /tmp/projectname.stats.sock --memory-report --processes 4 --threads 8
