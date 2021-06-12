FROM centos:7

LABEL maintainer="Naoto Minami"
LABEL repository="https://github.com/chlorochrule/solrcloud-development-box"

ARG LUCENE_REPOSITORY="https://github.com/chlorochrule/lucene"
ARG LUCENE_CHECKOUT="main"

ARG SOLR_REPOSITORY="https://github.com/chlorochrule/solr"
ARG SOLR_CHECKOUT="SNAPSHOT"

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk" \
    SOLR_JETTY_HOST="0.0.0.0" \
    SOLR_USER="solr" \
    SOLR_UID="8983" \
    SOLR_GROUP="solr" \
    SOLR_GID="8983" \
    PATH="/opt/solr/bin:$PATH" \
    SOLR_INCLUDE="/etc/default/solr.in.sh" \
    SOLR_HOME="/var/solr/data" \
    SOLR_PID_DIR="/var/solr" \
    SOLR_LOGS_DIR="/var/solr/logs" \
    LOG4J_PROPS="/var/solr/log4j2.xml"

RUN set -ex && \
    groupadd -r --gid $SOLR_GID $SOLR_GROUP && \
    useradd -r --uid $SOLR_UID --gid $SOLR_GID $SOLR_USER && \
    yum install git java-11-openjdk java-11-openjdk-devel -y && \
    mkdir /workspace && \
    cd /workspace && \
    git clone $LUCENE_REPOSITORY lucene && \
    cd lucene && \
    git checkout $LUCENE_CHECKOUT && \
    ./gradlew mavenToLocalRepo && \
    cd .. && \
    git clone $SOLR_REPOSITORY solr && \
    cd solr && \
    git checkout $SOLR_CHECKOUT && \
    ./gradlew assemble && \
    ./gradlew dev && \
    rm -rf /opt/solr && \
    cp -r solr/packaging/build/dev /opt/solr && \
    chown -R 0:0 /opt/solr && \
    find /opt/solr -type d -print0 | xargs -0 chmod 0755 && \
    find /opt/solr -type f -print0 | xargs -0 chmod 0644 && \
    chmod -R 0755 /opt/solr/bin /opt/solr/contrib/prometheus-exporter/bin/solr-exporter /opt/solr/server/scripts/cloud-scripts && \
    cp /opt/solr/bin/solr.in.sh /etc/default/solr.in.sh && \
    chown 0:0 /etc/default/solr.in.sh && \
    chmod 0664 /etc/default/solr.in.sh && \
    mkdir -p $SOLR_HOME $SOLR_LOGS_DIR && \
    cp /opt/solr/server/solr/solr.xml /opt/solr/server/solr/zoo.cfg $SOLR_HOME && \
    cp /opt/solr/server/resources/log4j2.xml $LOG4J_PROPS && \
    chown -R $SOLR_USER:0 /var/solr && \
    yum clean all && \
    rm -rf /var/cache/yum && \
    cd / && \
    rm -rf /workspace

VOLUME /var/solr
EXPOSE 8983
WORKDIR /opt/solr
USER $SOLR_USER

CMD /opt/solr/bin/solr start -c -f
