#! /bin/sh

artifact_name=$1
artifact_name=`echo $artifact_name | tr , _`
artifact_name=`echo $artifact_name | tr : _`
artifact_name=use_cases_${artifact_name}
echo $artifact_name