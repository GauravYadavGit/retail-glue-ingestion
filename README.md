# 🏗️ Retail Glue Ingestion Pipeline  
**End-to-End AWS Data Ingestion with Terraform & GitHub Actions CI/CD**

---

## 📌 Overview

This project demonstrates a **production-style data ingestion pipeline** built on AWS using **Infrastructure as Code (Terraform)** and **CI/CD automation (GitHub Actions)**.

The pipeline ingests data into **Amazon S3**, processes it via **AWS Glue**, and uses **AWS Lambda** as an orchestration layer.  
The entire infrastructure lifecycle is managed using Terraform, with **PR-based CI** and **main-branch-only CD**, closely mirroring real industry practices.

> 🎯 This project is designed as a **portfolio-grade system**, focusing on correctness, automation, and clear architectural decisions.

---

## 🧠 Key Objectives

- Build an end-to-end AWS ingestion pipeline using **Terraform**
- Implement **realistic CI/CD workflows** for infrastructure
- Separate **validation (CI)** from **deployment (CD)**
- Follow **industry-aligned Git workflows**
- Understand and document **Terraform state & deployment trade-offs**

---

## 🏛️ Architecture Overview

### Core AWS Components

- **Amazon S3**
  - Storage for raw and processed data
- **AWS Glue**
  - ETL job for data transformation
- **AWS Lambda**
  - Triggers and orchestrates Glue jobs
- **IAM**
  - Service roles for Lambda and Glue

### Automation & Tooling

- **Terraform** – Infrastructure as Code
- **GitHub Actions** – CI/CD automation
- **GitHub Secrets** – Secure credential management

---

## 📁 Repository Structure

```text
.
├── .github/
│   └── workflows/
│       ├── terraform-ci.yml     # CI: validate & plan on PRs
│       └── terraform-cd.yml     # CD: apply on main
│
├── terraform/
│   ├── lambda/
│   │   └── handler.py           # Lambda source code
│   ├── lambda.tf               # Lambda definition
│   ├── glue.tf                 # Glue job definition
│   ├── iam.tf                  # IAM roles & policies
│   ├── s3.tf                   # S3 bucket
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
│
├── README.md
└── requirements.txt


## 🧠 Terraform State Note

This project uses local Terraform state for simplicity.  
When CI/CD was introduced, an expected behavior was observed where existing AWS resources caused `EntityAlreadyExists` errors during deployment.  

In a production setup, Terraform state should be stored remotely (e.g., S3 with DynamoDB locking) to ensure idempotent deployments across CI/CD runners.  
The pipeline is intentionally designed to support this enhancement without structural changes.

