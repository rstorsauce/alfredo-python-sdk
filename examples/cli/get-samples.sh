#!/bin/bash

# If you don't have a token, please register as a new user
#	alfredo ruote users -C -i "{password: '****', email: alice@example.com}"
# Then, login using your credentials
#	alfredo login -i "{password: '****', email: alice@example.com}"

set -eu

function debug() {
	echo `TZ=utc LANG=C date` $* >&2
}

export JOB_CORES=1
export JOB_TIME=60
export CPU_STRESS='md5sum /dev/zero ; printenv'

export RUOTE_ROOT='https://apitest.rstor.io'
# export RUOTE_ROOT='https://a9ba69a2.ngrok.io'
# export RUOTE_ROOT='http://localhost:8000'

SLEEP_BETWEEN_APPS=60
SLEEP_WAIT_FINISH=35
SLEEP_WAIT_PERF=20

debug "Checking tools"
jq --version   >/dev/null 2>&1
yq --version   >/dev/null 2>&1
alfredo -help  >/dev/null 2>&1
uniqueid=.`date -u +%s.%N`

alfredo login < logindata.txt

user=`alfredo ruote users me | yq .email -r`
debug "Logged in as $user"

mkdir -p apps
mkdir -p queues
mkdir -p jobs
mkdir -p perf
mkdir -p telemetry

function get_queues() {
	alfredo ruote queues -o id,name
}

function get_queue_by_id() {
	debug "Retrieving information of queue $1"
	alfredo ruote queues id:$1 -o id,name
}

function get_apps() {
	# alfredo ruote apps -o id,name
	cat <<EOF
- id: 301
  name: Amber
EOF
}

function get_app_by_id() {
	debug "Retrieving information of app $1"
	alfredo ruote apps id:$1 -o id,name
}

function get_job_by_id() {
	alfredo ruote jobs id:$1
}

function names() {
	yq '.[]|.name' -r
}

function ids() {
	yq '.[]|.id' -r
}

function job() {
	app=$1
	queue=$2
	cat<<EOF
app: $1
queue: $2
name: rober-perf-a$1-q$2-`date -u +%y%m%d%H%M%S`
run_script: timeout $JOB_TIME $CPU_STRESS ; printenv
expected_runtime: `expr $JOB_TIME + 120`
num_cores: $JOB_CORES
EOF
}

function main() {
	app_ids=`get_apps | ids`
	queue_ids=`get_queues | ids`

	for queue_id in $queue_ids
	do
		get_queue_by_id $queue_id > queues/$queue_id.yml
	done

	touch $uniqueid.jobs
	touch $uniqueid.finished

	for app_id in $app_ids
	do
		get_app_by_id $app_id > apps/$app_id.yml
		for queue_id in $queue_ids
		do
			debug "Launching app `yq .name apps/$app_id.yml` in queue `yq .name queues/$queue_id.yml`" # of cluster `yq .cluster.name queues/$queue_id.yml`
			(
				job $app_id $queue_id > jobs/input-$app_id-$queue_id.yml
				( cat jobs/input-$app_id-$queue_id.yml | alfredo ruote jobs -C > jobs/creation.yml ) || exit $?
				job_id=`yq .id jobs/creation.yml`
				mv jobs/creation.yml jobs/$job_id.yml
				echo $job_id >> $uniqueid.jobs
			) || (
				debug "exit code:" $?
				while read line
				do
					debug $line
				done < jobs/creation.yml
			)
		done
		sleep $SLEEP_BETWEEN_APPS
	done

	while [[ `wc -l < $uniqueid.jobs` != `wc -l < $uniqueid.finished` ]]
	do
		sleep $SLEEP_WAIT_FINISH
		for job_id in `cat $uniqueid.jobs`
		do
			if [[ ! `grep \^$job_id\$ $uniqueid.finished` ]]; then
				status=`get_job_by_id $job_id | yq .last_state -r`
				debug "Job $job_id has status $status"
				if [[ "$status" == @(Completed|Failed) ]]
				then
					echo $job_id >> $uniqueid.finished
				fi
				if [[ "$status" == @(Completed) ]]
				then
					echo $job_id >> $uniqueid.completed
				fi
			fi
		done
	done

	for job_id in `cat $uniqueid.completed`
	do
		getperf="alfredo ruote jobs id:$job_id perf"
		perffile="perf/perf-$job_id.tar"

		while ! $getperf > $perffile
		do
			debug "Trying to get perf data of job $job_id"
			sleep $SLEEP_WAIT_PERF
		done
		debug "Got perf data of job $job_id"

		telemetryfile=`tar -tf $perffile | grep telemetry.backup\$`
		tar -xf $perffile
		mv $telemetryfile telemetry/telemetry-$job_id.influx

		debug "Getting telemetry json summary of job $job_id"
		alfredo ruote jobs id:$job_id telemetry > telemetry/telemetry-$job_id.json
	done
}

main
