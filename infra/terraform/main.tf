provider "aws" {
  region = var.aws_region
}

# VPC Base
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "sellerscenter-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
}

# Cola SQS para Ingesta Asíncrona
resource "aws_sqs_queue" "sync_inbound_dlq" {
  name = "sync-inbound-dlq"
}

resource "aws_sqs_queue" "sync_inbound" {
  name                       = "sync-inbound"
  visibility_timeout_seconds = 300
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.sync_inbound_dlq.arn
    maxReceiveCount     = 3
  })
}

# Base de Datos PostgreSQL
resource "aws_db_instance" "postgres" {
  identifier             = "sellerscenter-db"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "16"
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = module.vpc.database_subnet_group
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  skip_final_snapshot    = true
}

# Cluster ECS Fargate
resource "aws_ecs_cluster" "main" {
  name = "sellerscenter-cluster"
}

# Ejemplo de Tarea Fargate (API)
resource "aws_ecs_task_definition" "api" {
  family                   = "sellerscenter-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([{
    name      = "api"
    image     = "${var.ecr_repository_url}:latest"
    essential = true
    portMappings = [{
      containerPort = 8000
      hostPort      = 8000
    }]
  }])
}
