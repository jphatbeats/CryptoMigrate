#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:."
export FLASK_ENV=production
export FLASK_APP=main_server.py
python main_server.py