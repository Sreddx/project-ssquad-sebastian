#!/bin/bash
TIMELINEPOST='name=bashScriptTest&email=bash@test.com&content=testpostcontent'

curl --request POST http://localhost:5000/api/timeline_post -d $TIMELINEPOST
echo "---Added new post---"
curl http://localhost:5000/api/timeline_post

curl --request DELETE http://localhost:5000/api/timeline_post -d 'name=bashScriptTest'

echo "---Deleted post---"
curl http://localhost:5000/api/timeline_post
