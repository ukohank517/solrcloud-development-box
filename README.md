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
docker-compose exec solr1 /opt/solr/server/scripts/cloud-scripts/zkcli.sh -zkhost zoo:2181 -cmd upconfig -confdir /opt/solr/server/solr/configsets/wikipedia/conf -confname wikipedia
# create collection
curl 'localhost:8983/solr/admin/collections?action=CREATE&name=wikipedia&numShards=2&replicationFactor=2&maxShardsPerNode=2&collection.configName=wikipedia'
```

### Feed documents

Japanese wikipedia dataset is able to be got from [here](https://dumps.wikimedia.org/jawiki/). However, the dataset is formatted by complex XML.
The dataset converted as feedable JSON is able to be got from [here](https://drive.google.com/file/d/1KbRqykxvNRPkEZrznObf6uvCR1YIXB3A/view?usp=sharing).

NOTE: The original dataset of converted dataset is jawiki-20210601-pages-articles-multistream.xml.bz2

1. Download [JSON dataset](https://drive.google.com/file/d/1KbRqykxvNRPkEZrznObf6uvCR1YIXB3A/view?usp=sharing)

2. unzip dataset
```bash
du wikipedia_ja.zip
# 2841736 wikipedia_ja.zip

md5 wikipedia_ja.zip
# MD5 (wikipedia_ja.zip) = f90b2dcf8e640fda7ac942c95136cd40

unzip wikipedia_ja.zip
```

3. Feed using curl
```bash
# Feed all documents
for docs in $(ls wikipedia_ja/*.json); do curl -X POST -H 'Content-Type: application/json' --data-binary @$docs 'http://localhost:8983/solr/wikipedia/update?commit=true'; done
```

4. Check documents
```bash
curl 'localhost:8983/solr/wikipedia/select?q=*:*'
```

### Benchmark using JMeter

1. Create `queries.txt` using luke handler
```bash
curl -fsSL 'localhost:8983/solr/wikipedia/admin/luke?show=all&numTerms=10000&fl=text' | jq -r .fields.text.topTerms | grep '"' | sed -e 's/[" ,]//g' > queries_tmp.txt
```

2. Convert to Solr query
```bash
mkdir -p jmeter/benchmarks
jmeter/bin/create_wikipedia_queries.py queries_tmp.txt > jmeter/benchmarks/queries.txt
rm queries_tmp.txt
```

3. Run `benchmark-solr` script
```bash
docker-compose exec -u root jmeter benchmark-solr -c wikipedia -z zoo:2181 -q /var/jmeter/benchmarks/queries.txt -t 233 -d 60 --extract-expression '$.response.numFound' --extract-expression '$.responseHeader.QTime' --clean
```

4. See `report.txt`
```bash
cat jmeter/benchmarks/benchmark-solr/*/report.txt
```
`report.txt` example
```
--- summary report ---
num requests: 6578
execution time: 59.671 [sec]
error (without timeout) count: 0
timeout count: 0
error (with timeout) rate: 0.0
throughput: 110.23780395837174 [rps]
           elapsed      bytes  sentBytes  Latency
min           4.00     679.00     169.00     4.00
50%ile       48.00   44198.00     186.00    47.00
75%ile      180.00   62605.75     186.00   177.00
95%ile      734.15  104636.80     204.00   728.15
99%ile     1162.92  161320.78     222.00  1157.69
99.9%ile   1557.27  272524.30     240.00  1557.27
99.99%ile  1894.05  321512.07     258.00  1872.00
max        1971.00  330710.00     258.00  1970.00
mean        159.69   50264.35     186.80   157.57
std         248.78   30548.91       9.68   247.28
--- end report ---
```

#### Java Flight Recorder during benchmarking
```bash
docker-compose exec -u solr solr1 start-jfr.sh 60  # 60sec
ls solr/mnt/solr1/benchmarks/solr.jfr
```

### Graceful Shutdown
```bash
docker-compose exec -u solr solr1 solr stop -all
docker-compose exec -u solr solr2 solr stop -all
docker-compose down
```

### Prometheus

Access: `localhost:9090`

### Grafana

1. Access`localhost:3000`
2. Create Data sources of Prometheus (URL is `http://prometheus:9090`)
3. Import [dashboard](https://github.com/apache/solr/blob/main/solr/prometheus-exporter/conf/grafana-solr-dashboard.json)

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

1. Fix `gradle/globals.gradle`.

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
-org.apache.lucene:*=9.1.0
+org.apache.lucene:*=9.3.0-SNAPSHOT
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
