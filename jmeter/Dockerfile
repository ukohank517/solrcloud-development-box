FROM centos:7

LABEL maintainer="Naoto Minami"
LABEL repository="https://github.com/chlorochrule/solrcloud-development-box"

ARG JMETER_VERSION="5.4.3"

ENV JMETER_HOME="/opt/apache-jmeter-${JMETER_VERSION}" \
    JMETER_DOWNLOAD_URL="https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz" \
    PATH="${PATH}:${JMETER_HOME}/bin"

RUN set -ex && \
    yum install java-11-openjdk python3 -y && \
    pip3 install pip -U && \
    pip3 install jinja2 kazoo pandas && \
    mkdir /workspace && \
    curl -fsSL -o "/workspace/apache-jmeter-${JMETER_VERSION}.tgz" "${JMETER_DOWNLOAD_URL}" && \
    mkdir -p /opt && \
    tar xzvf "/workspace/apache-jmeter-${JMETER_VERSION}.tgz" -C /opt && \
    curl -fsSL -o "${JMETER_HOME}/lib/ext/jmeter-plugins-manager.jar" "https://jmeter-plugins.org/get/" && \
    curl -fsSL -o "${JMETER_HOME}/lib/cmdrunner-2.3.jar" "http://search.maven.org/remotecontent?filepath=kg/apc/cmdrunner/2.3/cmdrunner-2.3.jar" && \
    java -cp "${JMETER_HOME}/lib/ext/jmeter-plugins-manager.jar" org.jmeterplugins.repository.PluginManagerCMDInstaller && \
    ${JMETER_HOME}/bin/PluginsManagerCMD.sh install "jpgc-tst=2.5" && \
    rm -rf /workspace

WORKDIR	"${JMETER_HOME}"

COPY --chown=0:0 --chmod=755 bin/benchmark-solr /usr/local/bin/benchmark-solr
COPY --chown=0:0 --chmod=644 bin/solr.jmx /usr/local/bin/solr.jmx

CMD ["tail","-f", "/dev/null"]
