#!/bin/bash
# PAIN
uwurandom > temp.txt &
uwurandom_pid=$!
sleep 0.35
kill $uwurandom_pid
cat temp.txt > msg.txt
rm temp.txt

