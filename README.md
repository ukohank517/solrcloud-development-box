## A Docker image for SolrCloud development

**Note: This repository is for Lucene and Solr developers. DO NOT USE AS PRODUCTION.**

Development environment for SolrCloud using Docker and Docker compose.
This repository provides customized build for any lucene commit and solr commit.

## How to use: create solr system

### prepare json data

Amazon Shopping Queries Dataset is able to be got from [here](https://github.com/amazon-science/esci-data).

This dataset is included as a submodule in this repository.

You can prepare json data by the following steps:

1. take the data from github, this step may take a long time

    ```bash
    git submodule update --init --recursive
    ```

2. generate dataset
    ```bash
    cd data
    python3 create_shopping_data.py
    cd ..
    ```

then you can check you json data in folder data/amazonshopping

### launch dolr cloud

Run:

```bash
docker-compose up -d --build
```

You can see the solr system by accessing `localhost:8983` or `localhost:8984`.

The pull down menu 「Collection Selector」is empty now.

### Upload configsets and create collection

Configsets of amazon shopping data collection can be uploaded by:

```bash
# upload configsets
docker-compose exec solr1 /opt/solr/server/scripts/cloud-scripts/zkcli.sh -zkhost zoo:2181 -cmd upconfig -confdir /opt/solr/configsets/amazonshopping -confname amazonshopping
# create collection
curl 'localhost:8983/solr/admin/collections?action=CREATE&name=amazonshopping&numShards=2&replicationFactor=2&maxShardsPerNode=2&collection.configName=amazonshopping'
```

The file `solr/configsets/amazonshopping` is created base to the json file in `data/amazonshopping/**.json`,

The `field` defines every fields in json file, with the primary key named `example_id`.

Now, access to `localohst:8983`, you can find the `amazonshopping` included in the pull down menu 「Collection Selector」.

※ Here, you can find solr API [here](https://solr.apache.org/guide/7_1/coreadmin-api.html#coreadmin-create).
### Feed documents

The json file prepared before can be fee by curl command:
```bash
# Feed all documents
for docs in $(ls ./data/amazonshopping/*.json); do curl -X POST -H 'Content-Type: application/json' --data-binary @$docs 'http://localhost:8983/solr/amazonshopping/update?commit=true'; done
```

Access to `http://localhost:8983/solr/#/amazonshopping/query`, press `Execute Query` button and you can randomly get 10 json data.

## How to use: Benchmark using JMeter

1. Create Solr query
```bash
mkdir -p jmeter/benchmarks
cd data
python3 create_shopping_query.py > ../jmeter/benchmarks/queries.txt
cd ..
```

3. Run `benchmark-solr` script
```bash
docker-compose exec -u root jmeter benchmark-solr -c amazonshopping -z zoo:2181 -q /var/jmeter/benchmarks/queries.txt -t 233 -d 60 --extract-expression '$.response.numFound' --extract-expression '$.responseHeader.QTime' --clean
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
