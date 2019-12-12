#!/bin/bash

# trap ctrl-c and call exit()
trap exit INT

RUNNING=1

function exit() {
	# if [ $RUNNING == 0 ]; then	
	# 	echo "Already stopping monitoring !"
	# fi
	echo "Stopping monitoring"
	pkill mysqld
	pkill nethogs
	pkill pidstat
	pkill perf
	RUNNING=0
	echo "Formatting files"
	# tail -n +3 pidstat.log | head -n 1 > pidstat-formatted.log
	# tail -n +3 pidstat.log | awk 'NR == 1 || NR % 3 == 0' >> pidstat-formatted.log
	echo "Done"
}

perf stat -I 1000 -a -o ./logs/perf.log -e cache-references,cache-misses,page-faults mysqld &
sleep 1

ifpps -lpcd enp0s25 > ./logs/ifpps.dat &
# nethogs -t -d 1 > nethogs.log &

pidstat -dhrH -p $(pgrep mysqld) 1 &> ./logs/pidstat.log &

while [ $RUNNING == 1 ]; do
	echo "Monitoring..."
	sleep 5
done
