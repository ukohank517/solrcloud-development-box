#!/bin/bash
mkdir -p /opt/mnt/benchmark
rm -f /opt/mnt/benchmark/solr.jfr

jcmd "$(cat /var/solr/solr-8983.pid)" JFR.start duration="$1"s filename=solr.jfr
