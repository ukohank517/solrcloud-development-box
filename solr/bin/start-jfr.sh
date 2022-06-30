#!/bin/bash
mkdir -p /var/solr/benchmarks
rm -f /var/solr/benchmarks/solr.jfr

jcmd "$(cat /var/solr/solr-8983.pid)" JFR.start duration="$1"s filename=/var/solr/benchmarks/solr.jfr
