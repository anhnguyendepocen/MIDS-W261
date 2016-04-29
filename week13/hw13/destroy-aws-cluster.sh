#!/bin/sh
aws emr terminate-clusters --cluster-ids $(<cluster_id.txt)
