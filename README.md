# real-time-data-processing
Service that Receive packets of data in real-time and pass this on to an ancillary service for processing,Collate the output from the ancillary service for a particular Primary Resource ID into a single data packet. And once all data packets for a particular Resource are received, pass on the collated output data further for downstream processing with minimum latency by calling a webhook.


# Components Included
  1. Real time data receiver : Receive Data from AWS-Kinesism or Kafka.
  2. Data Transformer : Transform raw data into service consumable data.
  3. Data Down Streamer : Send transformed data to other servies to consume.

# Tech Inclusions

  1. Django Framework
  2. Celery Worker 
  3. Celery Beat
  4. AWS - SQS
  5. AWS - Kinesis
  6. Postgres DB
  
# Architecture
  
  1. Read Real time data from AWS-KINESIS/ KAFKA topic ( Implemented scheduler to read topics via celery-beat )
  2. Store data packet into database (used postgres). [ NO data drop ]
  3. Push raw data to queue (AWS-SQS: Publisher)
  4. Process data packets to transform into required data format (celery-worker: AWS-SQS.fifo consumner)
  5. Store processed data wrt ID's.
  6. Check for last_chunk_flag , If true downstream processed data to other consumer services. (AWS-SQS.fifo queue).

# How to use?

  System/ Machine Pre-requisites:
    1. Docker
    2. Python3
    
  Commands:
    1. docker-compose build
    2. docker-compose up -d
    
