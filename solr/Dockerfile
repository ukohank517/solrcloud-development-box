FROM centos:7

LABEL maintainer="Naoto Minami"
LABEL repository="https://github.com/chlorochrule/solrcloud-development-box"

ARG LUCENE_REPOSITORY="https://github.com/chlorochrule/lucene"
ARG LUCENE_CHECKOUT="branch_9x"

ARG SOLR_REPOSITORY="https://github.com/chlorochrule/solr"
ARG SOLR_CHECKOUT="SNAPSHOT"

ARG SOLR_INSTALL_DIR="/opt/solr"

ENV SOLR_JETTY_HOST="0.0.0.0" \
    SOLR_USER="solr" \
    SOLR_UID="8983" \
    SOLR_GROUP="solr" \
    SOLR_GID="8983" \
    PATH="$SOLR_INSTALL_DIR/bin:$PATH" \
    SOLR_INCLUDE="/etc/default/solr.in.sh" \
    SOLR_HOME="/var/solr/data" \
    SOLR_PID_DIR="/var/solr" \
    SOLR_LOGS_DIR="/var/solr/logs" \
    LOG4J_PROPS="/var/solr/log4j2.xml"

RUN set -ex && \
    groupadd -r --gid $SOLR_GID $SOLR_GROUP && \
    useradd -r --uid $SOLR_UID --gid $SOLR_GID $SOLR_USER && \
    yum install https://cdn.azul.com/zulu/bin/zulu-repo-1.0.0-1.noarch.rpm -y && \
    yum install which git zulu17-jdk -y && \
    mkdir /workspace && \
    cd /workspace && \
    git clone $LUCENE_REPOSITORY lucene && \
    cd lucene && \
    git checkout $LUCENE_CHECKOUT && \
    ./gradlew mavenToLocal && \
    cd .. && \
    git clone $SOLR_REPOSITORY solr && \
    cd solr && \
    git checkout $SOLR_CHECKOUT && \
    ./gradlew assemble && \
    ./gradlew dev && \
    mkdir -p $SOLR_INSTALL_DIR && \
    rm -rf $SOLR_INSTALL_DIR && \
    cp -r solr/packaging/build/dev $SOLR_INSTALL_DIR && \
    chown -R 0:0 $SOLR_INSTALL_DIR && \
    find $SOLR_INSTALL_DIR -type d -print0 | xargs -0 chmod 0755 && \
    find $SOLR_INSTALL_DIR -type f -print0 | xargs -0 chmod 0644 && \
    chmod -R 0755 $SOLR_INSTALL_DIR/bin $SOLR_INSTALL_DIR/prometheus-exporter/bin/solr-exporter $SOLR_INSTALL_DIR/server/scripts/cloud-scripts && \
    cp $SOLR_INSTALL_DIR/bin/solr.in.sh /etc/default/solr.in.sh && \
    chown 0:0 /etc/default/solr.in.sh && \
    chmod 0664 /etc/default/solr.in.sh && \
    mkdir -p $SOLR_HOME $SOLR_LOGS_DIR && \
    cp $SOLR_INSTALL_DIR/server/solr/solr.xml $SOLR_INSTALL_DIR/server/solr/zoo.cfg $SOLR_HOME && \
    cp $SOLR_INSTALL_DIR/server/resources/log4j2.xml $LOG4J_PROPS && \
    chown -R $SOLR_USER:$SOLR_GROUP /var/solr && \
    chown -R $SOLR_USER:$SOLR_GROUP $SOLR_INSTALL_DIR && \
    yum clean all && \
    rm -rf /var/cache/yum && \
    cd / && \
    rm -rf /workspace

COPY --chown=$SOLR_USER:$SOLR_GROUP bin/docker-entrypoint.sh $SOLR_INSTALL_DIR/bin/docker-entrypoint.sh
COPY --chown=$SOLR_USER:$SOLR_GROUP bin/start-jfr.sh $SOLR_INSTALL_DIR/bin/start-jfr.sh

VOLUME /var/solr
EXPOSE 8983
WORKDIR /opt/solr
USER $SOLR_USER

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/opt/solr/bin/solr", "start", "-c", "-f"]
