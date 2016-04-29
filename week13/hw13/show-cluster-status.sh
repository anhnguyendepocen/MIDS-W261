#!/bin/sh
aws emr describe-cluster --cluster-id $(< cluster_ids.txt) | grep STATUS
