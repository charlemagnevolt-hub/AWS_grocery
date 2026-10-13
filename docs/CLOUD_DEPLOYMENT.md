# GroceryMate Cloud Deployment

## Project Overview

GroceryMate is a full stack e-commerce application deployed as part of the Masterschool Cloud Engineering track.

The project demonstrates local development, containerization and deployment with managed AWS infrastructure.

## Architecture

```text
User
  |
  v
Amazon EC2
  |
  v
Docker container running Flask and Gunicorn
  |
  +--> Amazon RDS for PostgreSQL data
  |
  +--> Amazon S3 for avatar storage
```

## Technology Stack

* Python 3.12
* Flask
* Gunicorn
* React
* Docker
* Docker Compose
* PostgreSQL
* Amazon EC2
* Amazon RDS
* Amazon S3
* AWS IAM
* AWS Security Groups
* Git and GitHub

## Implementation Progress

### Week 1: Local Development

* Configured Python 3.12.
* Created a project-specific virtual environment.
* Started the Flask application locally.
* Verified the products API with HTTP status 200.

### Week 2: Amazon EC2

* Created an Amazon Linux 2023 EC2 instance.
* Created and secured an SSH key pair.
* Connected to the instance through SSH.
* Verified the operating system and Python environment.

### Week 3: Application Deployment

* Cloned the GroceryMate repository to EC2.
* Installed Python, Node.js and PostgreSQL.
* Imported the GroceryMate database.
* Deployed the backend and frontend.
* Configured Gunicorn and a system service.
* Made the application accessible through the EC2 network configuration.
* Configured a target group and an Application Load Balancer during the deployment exercise.

### Week 4: Docker

* Created a Dockerfile based on Python 3.12.
* Created a Docker Compose configuration.
* Built and started the GroceryMate backend container.
* Verified the containerized products API with HTTP status 200.
* Removed credentials from version-controlled configuration.

### Week 5: Amazon RDS

* Created a private PostgreSQL RDS instance.
* Configured network access between EC2 and RDS.
* Connected to RDS using SSL.
* Migrated the GroceryMate database to RDS.
* Verified four database tables, 318 products and 1,235 reviews.
* Reconfigured the Docker application to use RDS.

### Week 6: Infrastructure Preparation

* Created a dedicated infrastructure directory.
* Documented the intended Infrastructure as Code structure.
* Reviewed AWS costs and resource usage.

The infrastructure directory is currently a foundation for future Terraform configuration. It does not yet represent a complete automated AWS deployment.

### Week 7: Amazon S3

* Created a private S3 bucket.
* Kept S3 Block Public Access enabled.
* Created a dedicated EC2 IAM role.
* Restricted the IAM permissions to the GroceryMate bucket.
* Configured GroceryMate to use S3 storage.
* Uploaded application avatar files to the avatars prefix.
* Verified S3 access through the EC2 IAM role without static AWS access keys.
* Confirmed that the application continued to return HTTP status 200.

## Security Decisions

* Secrets are stored in local environment files.
* Environment files are excluded from Git.
* No AWS access keys are stored in the repository.
* EC2 accesses S3 through an IAM role.
* The S3 bucket remains private.
* RDS is not publicly accessible.
* Security Groups restrict inbound network access.
* Database connections use SSL.

## Local Docker Start

Create the required local environment files before starting the application.

```powershell
docker compose up --build -d
docker compose ps
```

Test the application:

```powershell
Invoke-WebRequest `
  -UseBasicParsing `
  http://127.0.0.1:5000/api/products/all_products |
Select-Object StatusCode
```

Expected result:

```text
StatusCode
200
```

## Repository Structure

```text
backend/              Flask backend
frontend/             React frontend
infrastructure/       Infrastructure as Code foundation
docs/                 Cloud deployment documentation
docker-compose.yml    Docker Compose configuration
README.md             Main project documentation
```

## Verified Results

* GroceryMate runs locally with Python 3.12.
* GroceryMate runs inside Docker.
* GroceryMate was deployed to Amazon EC2.
* PostgreSQL data was migrated to Amazon RDS.
* Application files were stored in Amazon S3.
* The products API returned HTTP status 200 after the cloud integrations.

## Author

Dr. Torsten Bernasco

Masterschool Cloud Engineering Track
