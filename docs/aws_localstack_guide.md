# Guía Paso a Paso para configurar y probar SellersCenter con LocalStack (AWS Local)

Esta guía te explicará desde cero cómo levantar toda la infraestructura sin gastar 1 centavo en AWS.

## 1. ¿Qué es LocalStack?
LocalStack es un contenedor de Docker que "finge" ser AWS. En lugar de mandar peticiones a internet para crear una cola SQS o guardar una foto en S3, todo ocurre dentro de tu computadora.

## 2. Requisitos Previos
1. Instalar **Docker Desktop** (Asegúrate de que el icono de la ballena esté verde).
2. Tener Python instalado.
3. Instalar la herramienta `awslocal` en tu consola (esto es el AWS CLI pero configurado para apuntar a LocalStack):
   `pip install awscli-local`

## 3. Levantar la Infraestructura
Abrir la terminal en la carpeta `infra/docker/` y ejecutar:
`docker-compose up -d`

Esto iniciará:
1. La base de datos PostgreSQL.
2. Redis (Caché).
3. LocalStack (Fingiendo ser AWS SQS, S3, SecretsManager).

El archivo `init-localstack.sh` se ejecutará automáticamente creando las colas y buckets necesarios.

## 4. Validando Recursos
Para comprobar que AWS "falso" está funcionando, ejecuta en tu terminal local:

**Ver colas creadas (SQS):**
`awslocal sqs list-queues`
*Deberías ver `incoming-orders`, `sync-outbound`, etc.*

**Ver buckets creados (S3):**
`awslocal s3 ls`
*Deberías ver `sc-frontend-dev` y `sc-media-dev`.*

## 5. Corriendo el Proyecto
Una vez validada la infra:
1. Instalar dependencias del proyecto: `pip install -r src/requirements.txt`
2. Correr migraciones de base de datos de Django: `python src/manage.py migrate`
3. Iniciar el worker de Celery: `celery -A config worker -l info`
4. Iniciar el servidor web: `python src/manage.py runserver`

¡Y listo! Al enviar mensajes a Celery, este se conectará a LocalStack en el puerto 4566 fingiendo ir a AWS.
