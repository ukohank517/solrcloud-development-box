#!/bin/bash
#
# docker-entrypoint.sh for SolrCloud

set -e

# Merge configset file
for d in $(ls -d /opt/mnt/solr/configsets/*); do
  rm -rf "${d/opt\/mnt/opt/solr/server}"
  ln -nsf "$d" "${d/opt\/mnt/opt/solr/server}"
done;

# solr.xml
if [ -f /opt/mnt/solr/solr.xml ]; then
    ln -sf /opt/mnt/solr/solr.xml /opt/solr/server/solr/solr.xml
fi

# zoo.cfg
if [ -f /opt/mnt/solr/zoo.cfg ]; then
    ln -sf /opt/mnt/solr/zoo.cfg /opt/solr/server/solr/zoo.cfg
fi

# execute command passed in as arguments.
# The Dockerfile has specified the PATH to include.
exec "$@"
