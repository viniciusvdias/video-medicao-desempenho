#! /usr/bin/env bash

free && sync && echo 3 > /proc/sys/vm/drop_caches && free
