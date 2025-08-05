#!/bin/bash
export PORT=${PORT:-5000}
export FLASK_ENV=production
export FLASK_APP=main_server.py
python main_server.py