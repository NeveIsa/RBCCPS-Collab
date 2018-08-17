#!/bin/sh
curl -v http://localhost:8001/cat?id=$1 --user : -X DELETE -H "pwd:$2"
#delete_item 70b3d58ff0031d2c local123
#curl -v http://localhost:8001/cat?id=70b3d58ff0031d2c --user : -X DELETE -H "pwd:local123"

