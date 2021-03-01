#!/bin/bash

DEBUG=${DEBUG:=1}
export HTTP_HOST="${HTTP_HOST:=0.0.0.0}"
export HTTP_PORT="${HTTP_PORT:=5000}"
export VERBOSE=1

if [ ! -f venv/bin/activate ]; then
  echo "Virtualenv not created!"
  exit 1
fi

source venv/bin/activate

export PYTHONPATH="${PYTHONPATH}:itflex"
python -m itflex.run

