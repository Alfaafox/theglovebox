#!/bin/bash

source venv/bin/activate

pkill -f uvicorn 2>/dev/null

sleep 1

uvicorn app.main:app --reload
