#!/bin/bash
# PAIN
uwurandom > temp.txt &
uwurandom_pid=$!
sleep 0.05
kill $uwurandom_pid
cat temp.txt | head -c 1024 > msg.txt
rm temp.txt

