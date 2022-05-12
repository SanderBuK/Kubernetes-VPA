while [ true ]
do
    for i in $(seq 20000)
    do
        echo ${i}
        sleep 0.0005s
    done
    sleep 30s
done