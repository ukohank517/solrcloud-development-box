## A Docker image for SolrCloud development

**Note: This repository is for Lucene and Solr developers. DO NOT USE AS PRODUCTION.**

Development environment for SolrCloud using Docker and Docker compose.
This repository provides customized build for any lucene commit and solr commit.

## How to use

Run:

```bash
docker-compose up -d
```

With build:

```bash
docker-compose up -d --build
```

and access `localhost:8983` or `localhost:8984`.

### Upload configsets and create collection

[Configsets of wikipedia collection](https://github.com/chlorochrule/solrcloud-development-box/tree/main/solr/mnt/solr/configsets/wikipedia/conf)
can be uploaded by:

```bash
# upload configsets
docker-compose exec solr1 /opt/solr/server/scripts/cloud-scripts/zkcli.sh -zkhost zoo:2181 -cmd upconfig -confdir /opt/mnt/solr/configsets/wikipedia/conf/ -confname wikipedia
# create collection
curl 'localhost:8983/solr/admin/collections?action=CREATE&name=wikipedia&numShards=2&replicationFactor=2&maxShardsPerNode=2&collection.configName=wikipedia'
```

### Prometheus

Access: `localhost:9090`

### Grafana

1. Access`localhost:3000`
2. Create Data sources of Prometheus (URL is `http://prometheus:9090`)
3. Import [dashboard](https://github.com/apache/solr/blob/main/solr/contrib/prometheus-exporter/conf/grafana-solr-dashboard.json)

## Customize for your development

Fix below environment variables:

```Dockerfile
ARG LUCENE_REPOSITORY="https://github.com/chlorochrule/lucene"  # Lucene repository you want to build
ARG LUCENE_CHECKOUT="main"  # Lucene branch, commit or tag

ARG SOLR_REPOSITORY="https://github.com/chlorochrule/solr"  # Solr repository you want to build
ARG SOLR_CHECKOUT="SNAPSHOT"  # Solr branch, commit or tag
```

## How to refer Lucene SNAPSHOT from Solr

When referencing a particular Lucene branch, for example `main`, from Solr, Gradle build settings of Solr must be fix.

1. Fix `gradle/defaults.gradle`.

```diff
@@ -24,6 +24,7 @@ allprojects {

   // Repositories to fetch dependencies from.
   repositories {
+    mavenLocal()
     mavenCentral()
     maven {
       name "LucenePrerelease${lucenePrereleaseBuild}"
```

2. Fix `version.props`.

```diff
@@ -87,7 +87,7 @@ org.apache.httpcomponents:httpmime=4.5.10
 org.apache.james:apache-mime4j*=0.8.3
 org.apache.kerby:*=1.0.1
 org.apache.logging.log4j:*=2.13.2
-org.apache.lucene:*=9.0.0-prerelease5
+org.apache.lucene:*=9.0.0-SNAPSHOT
 org.apache.opennlp:opennlp-tools=1.9.1
 org.apache.pdfbox:*=2.0.17
 org.apache.pdfbox:jempbox=1.8.16
```

3. Update dependencies.

```bash
./gradlew --write-locks
```

4. Check build success.

```bash
./gradlew assemble
```

## License

Apache-2.0 License

## Author

Naoto Minami
