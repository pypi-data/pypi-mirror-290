#!/bin/bash

export PYTHONPATH=./src:./tests
pytest tests/*.py
