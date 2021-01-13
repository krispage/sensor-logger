#!/bin/bash
inkscape -w 16 -h 16 -e 16.png logo.svg
inkscape -w 32 -h 32 -e 32.png logo.svg
inkscape -w 48 -h 48 -e 48.png logo.svg

convert 16.png 32.png 48.png static/favicon.ico
