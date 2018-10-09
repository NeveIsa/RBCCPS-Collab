#!/bin/bash
lasttime="0"
while [ 1 ]
do

	js=$(curl -s -H 'Content-Type: application/json' -XPOST 'elasticsearchserver:9200/fb/event/_search?pretty' -d '{"size": 1,"sort":{"timestamp":"desc"},"query":{"match_all":{}}}' | jq '.hits.hits[0]._source')
	event=$(echo $js | jq 'keys[0]')
	time=$(echo $js | jq '.timestamp')
	if [ "$lasttime" != "$time" ]; then
		echo ----------------------
		echo New event!
		
		if [[ $event == *"refill"* ]]; then
			eventTag="green"
			ledTrigger='{"led":{"green":1}}'
		elif [[ $event == *"service"* ]]; then
			eventTag="red"
			ledTrigger='{"led":{"red":1}}'
		elif [[ $event == *"break"* ]]; then
			eventTag="yellow"
			ledTrigger='{"led":{"red":1,"green":1}}'
		fi
	echo $eventTag
	echo ----------------------
	
	mosquitto_pub -t notify/annotation -m $ledTrigger
	sleep 5 && mosquitto_pub -t notify/annotation -m  '{"led":{"red":0,"green":0,"blue":0}}' &
	
	fi
	lasttime=$time
	
	sleep 0.5
done

