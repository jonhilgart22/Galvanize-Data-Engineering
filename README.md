# DSCI 6007: Distributed and Scalable Data Engineering

Welcome to Intro to Data Engineering!

_See [syllabus.md](syllabus.md) for the current syllabus._

## Schedule Overview
Organized by weeks and days:  
(_subject to change;  
see detailed schedule [below](#detailed-schedule)_)

1. [Welcome to Data Engineering](#week-1-welcome-to-data-engineering)  
(_N.B._ Class starts on a Thursday this minimester.)
    1. [Data Engineering Overview](1.1 - Course Overview)
    2. [How the Internet Works](1.2 - The Internet)
2. [Linux and the Cloud](#week-2-linux-and-the-cloud)
    1. [Virtualization](2.1 - Virtualization)
    2. [Linux](2.2 - Linux)
    3. [The Cloud](2.3 - The Cloud)
    4. [Intro to NoSQL](2.4 - Intro to NoSQL)
3. [SQL (The Lingua Franca of Data)](#week-3-sql-the-lingua-franca-of-data)
    1. [PostgreSQL](3.1 - PostgreSQL)
    2. [Relational Data Modeling](3.2 - Relational Data Modeling)
    3. [Message Brokers](3.3 - Message Brokers)
    4. [Review Day / Project Proposal Check-in](3.4 - Projects)
4. MapReduce (Divide-and-conquer for Distributed Systems)
    1. Distributed Processing
    2. The MapReduce Algorithm & Hadoop
    3. MapReduce Design Patterns
    4. Spark: Overview
5. Spark (What to add to your LinkedIn profile)
    1. Spark: DataFrames & Datasets
    2. Spark SQL
    3. NoSQL: Redshift and Cassandra
    4. Advanced Spark
6. Machine Learning at Scale  
(_N.B._ Monday's class moved to Wednesday on account of President's Day)
    1. (Tuesday) Review Day
    2. (Wednesday) MLlib: Overview & Collaborative Filtering
    3. MLlib: Latent Semantic Analysis
    4. Search
7. Streaming (Everyone **has to have** real-time)
    1. Spark Streaming: Part 1
    2. Spark Streaming: Part 2
    3. Probabilistic Data Structures: Bloom Filter & Count–min sketch
    4. Probabilistic Data Structures: HyperLogLog & Locality-sensitive hashing (LSH)
8. Final Project Presentation
    1. Review Day
    2. Final Project Work Session      
    3. Project Presentations: Day 1    
    4. Project Presentations: Day 2     

## Detailed Schedule

### Week 1: Welcome to Data Engineering  

| Day      | Readings | Lecture(s) | Assignment |
|:--------:|:-------- |:---------- |:---------- |
| Thursday | [Data Engineering Overview](1.1 - Course Overview/README.md) | 1. [Intro to Data Engineering](1.1 - Course Overview/lecture_intro_to_data_engineering.ipynb) <BR /> 2. [Intro to the Cloud](1.1 - Course Overview/lecture_intro_to_the_cloud.ipynb) | [Conencting to the Cloud with Python](1.1 - Course Overview/lab.md) |
| Friday   | [How the Internet Works](1.2 - The Internet/README.md) | [How the Web Works](http://slides.com/wesleyreid/how-the-web-works) | [Generating Reports](1.2 - The Internet/lab.md) |

### Week 2: Linux and the Cloud

| Day      | Readings | Lecture(s) | Assignment |
|:--------:|:-------- |:---------- |:---------- |
| Monday   | [Virtualization](2.1 - Virtualization/README.md) | [Virtualization & Docker](2.1 - Virtualization/lecture_virtualization.ipynb) | [Your Very Own Web Server](2.1 - Virtualization/lab.md) |
| Tuesday  | [\*NIX](2.2 - Linux/README.md) | [Linux](2.2 - Linux/lecture_linux.ipynb) | [Linux Intro](2.2 - Linux/lab.md) |
| Thursday | [Introduction to Clouds](2.3 - The Cloud/README.md) | 1. [The Cloud & AWS](2.3 - The Cloud/lecture_the_cloud2_EC2.ipynb) <BR /> 2. [EC2 & cron](2.3 - The Cloud/lecture_cron_ec2.ipynb) | [Move your Linux machine to the Cloud](2.3 - The Cloud/lab.md) |
| Friday | [Working with MongoDB](2.4 - Intro to NoSQL/README.md) | 1. [NoSQL for Dummies](2.4 - Intro to NoSQL/lecture_nosql_intro.ipynb) <BR /> 2. [Even more NoSQL](2.4 - Intro to NoSQL/lecture_mongoDB.ipynb) | [Streaming Tweets into Mongo](2.4 - Intro to NoSQL/lab.md) |

### Week 3: SQL (The Lingua Franca of Data)

| Day      | Readings | Lecture(s) | Assignment |
|:--------:|:-------- |:---------- |:---------- |
| Monday   | [Not Only SQL](3.1 - PostgreSQL/README.md) | 1. [Advanced Querying](3.1 - PostgreSQL/lecture_sql_advanced_querying.ipynb) <BR /> 2. [SQL Optimization](3.1 - PostgreSQL/lecture_sql_optimization.ipynb) | [RDS](3.1 - PostgreSQL/lab.md) |
| Tuesday  | [Relational Design](3.2 - Relational Data Modeling/README.md) | [Relational Database Modeling](3.2 - Relational Data Modeling/lecture_relational_model.ipynb) | [Data Modeling Practice](3.2 - Relational Data Modeling/lab.md) |
| Thursday | [I ♥ Logs](3.3 - Message Brokers/README.md) | [Apache Kafka](3.3 - Message Brokers/lecture_kafka.ipynb) | [Drinking from the Firehose](3.3 - Message Brokers/lab.md) |
| Friday   | [Projects](3.4 - Projects/README.md) | [Requirements](3.4 - Projects/project_proposal.ipynb) | [Proposal](3.4 - Projects/lab.md) |
