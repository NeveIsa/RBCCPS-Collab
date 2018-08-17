id=$(cat nexThing.json | jq '.id' | xargs echo)
echo "Found ID: $id"
#file=$(cat $1)
#file="$file"
#echo $file
sleep 2
curl -v http://server:8001/cat?id=$id -XPOST -H "no-check:1" -H "pwd: feynman" -H "Content-Type: application/json" --data @$1
