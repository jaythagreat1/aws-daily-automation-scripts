## Quick Start
Clone the repository:

```bash
git clone https://github.com/jaythagreat1/aws-daily-automation-scripts.git
cd aws-daily-automation-scripts
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure AWS credentials:

```bash
aws configure
```

Run any script:

```bash
python -m scripts.cost_anomaly_finder
python -m scripts.security_group_audit
python -m scripts.iam_permission_audit
python -m scripts.tag_compliance_report
python -m scripts.lambda_error_summary
python -m scripts.multi_region_inventory
```

# AWS Cloud Operations Automation

A lightweight automation toolkit designed to surface common operational issues in AWS environments related to **cost optimization, security exposure, IAM governance, tagging 
compliance, and system observability**.

The scripts automate a set of checks frequently performed by cloud and platform teams to maintain visibility into AWS infrastructure and identify potential risks or inefficiencies 
across environments.

Built with **Python and boto3**, the toolkit interacts directly with AWS APIs and produces simple CSV reports that can be used for auditing, troubleshooting, or integration into 
automation workflows.

---

# Capabilities

## Cost Visibility

Detects resources that may generate unnecessary cost:

- Stopped EC2 instances that still incur EBS charges
- Unattached EBS volumes
- Unassociated Elastic IP addresses
- NAT Gateways that may require cost review

---

## Security Group Auditing

Identifies security groups exposing infrastructure to the public internet (`0.0.0.0/0` or `::/0`) on sensitive ports such as:

- SSH (22)
- RDP (3389)
- MySQL (3306)
- PostgreSQL (5432)
- Redis (6379)
- MongoDB (27017)

---

## IAM Governance Checks

Surfaces common IAM hygiene issues including:

- Users without MFA enabled
- Access keys older than recommended rotation thresholds
- Inline policies attached to IAM users
- High privilege policies such as `AdministratorAccess`

---

## Tagging Compliance

Verifies that infrastructure resources include required governance tags:

- Name
- Environment
- Owner

These tags help support cost allocation, automation, and operational ownership.

---

## Lambda Observability

Scans CloudWatch logs for recent Lambda errors and generates reports showing:

- Functions with error activity
- Number of errors detected
- Sample error message

---

## Multi-Region Infrastructure Inventory

Scans all enabled AWS regions and generates an EC2 inventory report including:

- Region
- Instance ID
- Name tag
- Instance type
- Instance state

This provides quick visibility into deployed compute resources across an AWS environment.

---

# Technologies Used

- Python
- boto3
- AWS CLI
- Amazon EC2
- AWS IAM
- Amazon CloudWatch Logs

---

# Project Structure

aws-daily-automation-scripts
├── scripts
│ ├── utils.py
│ ├── cost_anomaly_finder.py
│ ├── security_group_audit.py
│ ├── iam_permission_audit.py
│ ├── tag_compliance_report.py
│ ├── lambda_error_summary.py
│ └── multi_region_inventory.py
│
├── output
│
├── requirements.txt
└── README.md


---

# Setup

Clone the repository:


git clone https://github.com/jaythagreat1/aws-daily-automation-scripts.git

cd aws-daily-automation-scripts


Create a virtual environment:


python3 -m venv venv
source venv/bin/activate


Install dependencies:


pip install -r requirements.txt


Configure AWS credentials:


aws configure
aws sts get-caller-identity


---

# Running the Scripts

Run scripts from the project root.

Example:


python -m scripts.cost_anomaly_finder
python -m scripts.security_group_audit
python -m scripts.iam_permission_audit
python -m scripts.tag_compliance_report
python -m scripts.lambda_error_summary
python -m scripts.multi_region_inventory


---

# Example Output

Each script generates timestamped CSV reports.

Example:


output/security_group_audit_2026-03-12_10-22-40.csv


Reports can be reviewed manually or integrated into monitoring workflows.

---

# Use Cases

These scripts can help teams:

- Identify potential cost inefficiencies
- Detect publicly exposed infrastructure
- Improve IAM security posture
- Enforce tagging standards
- Monitor Lambda runtime errors
- Maintain visibility into resources across AWS regions

---

# Future Improvements

Potential enhancements include:

- Multi-account scanning using AssumeRole
- Automated scheduling using EventBridge or GitHub Actions
- Slack or SNS alerting for critical findings
- Support for additional AWS services such as RDS, S3, DynamoDB, and EKS
- JSON report output for automation pipelines

---

# License

MIT License
