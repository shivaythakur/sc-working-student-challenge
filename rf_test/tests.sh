#!/usr/bin/env sh

# Hint: Add something here to wait until the server is ready  

'''URL="http://server:80/ready"  
REQUIRED_VALUE="YES" 
SLEEP_INTERVAL=5  

while true; do
 
    RESPONSE=$(curl -s "$URL")
    
    if echo "$RESPONSE" | grep -q "$REQUIRED_VALUE"; then
        echo "Server is now ready to test"
        break
    else
        echo "Server is not ready yet, checking again in $SLEEP_INTERVAL seconds..."
    fi
    
    sleep $SLEEP_INTERVAL


done'''

mkdir -p results

robot -d results test-server.robot
