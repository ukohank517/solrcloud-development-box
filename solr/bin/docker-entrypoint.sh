#!/bin/bash
#
# docker-entrypoint.sh for SolrCloud

set -e

# execute command passed in as arguments.
# The Dockerfile has specified the PATH to include.
exec "$@"
