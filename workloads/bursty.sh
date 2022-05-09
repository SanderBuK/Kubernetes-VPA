while [ true ]
do
    for i in $(seq 20000)
    do
        echo ${i}
        sleep 0.00005s
    done
    sleep 30s
done