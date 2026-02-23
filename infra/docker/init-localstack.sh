#!/bin/bash
echo "Inicializando recursos de LocalStack para SellersCenter..."
# Colas SQS
awslocal sqs create-queue --queue-name incoming-orders
awslocal sqs create-queue --queue-name incoming-orders-dlq
awslocal sqs create-queue --queue-name sync-outbound
awslocal sqs create-queue --queue-name sync-outbound-dlq

# Buckets S3
awslocal s3 mb s3://sc-frontend-dev
awslocal s3 mb s3://sc-media-dev

echo "Recursos inicializados con éxito."
