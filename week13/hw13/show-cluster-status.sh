#!/bin/sh
while :; do aws emr describe-cluster --cluster-id $(< cluster_ids.txt) | grep STATUS:; sleep 5s; done