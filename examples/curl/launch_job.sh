#!/bin/bash

set -e


# Get the vars API_ROOT and TOKEN from ~/.apivars.sh
. ~/.apivars.sh


# Check if TOKEN is set
if [[ -z "$TOKEN" ]];then
    echo "Empty TOKEN" >&2
    exit 1
fi


# Check if API_ROOT is set
if [[ -z "$API_ROOT" ]];then
    echo "Empty API_ROOT" >&2
    exit 1
fi


# Validate API_ROOT
echo "$API_ROOT" |grep '^https:' >/dev/null
if [[ $? -ne 0 ]];then
    echo 'API_ROOT must start with https:' >&2
    exit 1
fi


# Set the Queue
queue=8
echo "Using queue: $queue"
curl -H "Authorization: Token ${TOKEN}" \
    $API_ROOT/queues/$queue/ | grep 'id.*name.*"enabled":true'
if [[ $? -ne 0 ]];then
    echo "Invalid Queue" >&2
    exit 1
fi



# Set the app
app=352
echo "Using app: $app"
curl -H "Authorization: Token ${TOKEN}" \
    $API_ROOT/apps/$app/ | grep 'id.*name.*"enabled":true'
if [[ $? -ne 0 ]];then
    echo "Invalid App" >&2
    exit 1
fi


# Set time limit
time_seconds=600


# Create a job name
name=`date +%y.%m.%d.%H:%M:%S`
name="$USER-test-appname-$name"


# Launch the job
echo "Lauching: $name"
curl -H "Authorization: Token ${TOKEN}" \
     $API_ROOT/jobs/ \
     -d name=$name -d queue=$queue -d time_seconds=$time_seconds -d app=$app -d run_script="/run_test.sh"
