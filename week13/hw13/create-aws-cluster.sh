#!/bin/sh
aws emr create-cluster --release-label emr-4.6.0 --use-default-roles \
--name HW13Cluster --applications Name=SPARK --log-uri s3://hadoopspark/logs/ \
--ec2-attributes KeyName=AWS_EC2_VAGRANT \
--bootstrap-action Path=s3://elasticmapreduce/bootstrap-actions/run-if,Args=["instance.isMaster=true","s3://hadoopspark/bootstrap/bootstrap.sh"] \
--instance-groups InstanceGroupType=MASTER,InstanceType=m3.xlarge,InstanceCount=1,BidPrice=0.04 \
InstanceGroupType=CORE,BidPrice=0.04,InstanceType=m3.xlarge,InstanceCount=2 > cluster_ids.txt
