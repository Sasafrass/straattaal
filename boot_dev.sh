#!/bin/bash
source venv/bin/activate
flask db upgrade
python tests.py
