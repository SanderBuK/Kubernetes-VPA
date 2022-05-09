for i in $(seq 100)
do
    export i
    timeout 60 /bin/bash -c -- 'while true; do echo $i; sleep_time=$(printf "0.%05ds" $((100000/(2**$i)))); sleep ${sleep_time}; done;'
done