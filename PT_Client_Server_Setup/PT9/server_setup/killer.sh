#!/bin/bash

kill -9 $(lsof -t -i:9050)
kill -9 $(lsof -t -i:5300)
