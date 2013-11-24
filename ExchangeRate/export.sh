#!/bin/bash
function scrapy_crawl {
	local SYSTEM;
	local TIME;
	TIME="$1";
	SYSTEM="$2";
	
	echo "" > "output/${TIME}-${SYSTEM}.json"
	scrapy crawl "${SYSTEM}" --output="output/${TIME}-${SYSTEM}.json" --output-format="json" -L "ERROR";
	#scrapy crawl "${SYSTEM}" --output="output/${TIME}-${SYSTEM}.json" --output-format="json";
}

# chdor to the script directory
F="`readlink -f $0`"
DIR=`dirname "$F"`
cd "$DIR"

mkdir "output"

#TIME=`date "+%Y%m%d-%H%M%S"`
#TIME=`date "+%Y%m%d-%H0000"`
M=`date "+%M"|sed s/^0//`
M=`printf "%02d" $(( (M/5)*5 ))`
TIME=`date "+%Y%m%d-%H${M}00"`


scrapy_crawl "$TIME" "BNR"
scrapy_crawl "$TIME" "BCR"
scrapy_crawl "$TIME" "AlphaBank"
scrapy_crawl "$TIME" "RIB"
scrapy_crawl "$TIME" "CEC"
scrapy_crawl "$TIME" "Transilvania"
