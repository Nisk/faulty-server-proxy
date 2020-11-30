#!/bin/bash

while [ 1 ]
do
	echo -e "\n"
    curl -X GET localhost:5000/v1/VIP/2
	echo -e "----------------------\n"
done
