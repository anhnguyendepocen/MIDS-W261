#!/bin/sh
aws emr create-cluster --release-label emr-4.6.0 --use-default-roles \
--name HW13Cluster --applications Name=SPARK Name=Zeppelin-Sandbox --log-uri s3://hadoopspark/logs/ \
--ec2-attributes KeyName=AWS_EC2_VAGRANT --instance-type m3.xlarge \
--instance-count 6 --use-default-roles > cluster_id.txt

