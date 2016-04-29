#!/bin/sh
aws emr create-cluster --release-label emr-4.6.0 --use-default-roles \
--name HW13Cluster --applications Name=SPARK Name=Zeppelin-Sandbox --log-uri s3://hadoopspark/logs/ \
--ec2-attributes KeyName=AWS_EC2_VAGRANT \
--instance-groups InstanceGroupType=MASTER,InstanceType=m3.xlarge,InstanceCount=1,BidPrice=0.05 \
InstanceGroupType=CORE,BidPrice=0.05,InstanceType=m3.xlarge,InstanceCount=4 > cluster_id.txt

