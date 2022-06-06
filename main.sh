#!/bin/bash
set -ex
rm -f log.txt
rm -rf html_results
mkdir html_results
python mini_spider.py