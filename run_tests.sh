#!/bin/bash

set -eux

coverage erase

nosetests --rednose --with-coverage --cover-package=alfredo --cover-html --stop --verbosity 2

