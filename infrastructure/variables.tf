variable "aws_region" {
  description = "AWS region used for the GroceryMate deployment."
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Name prefix for AWS resources."
  type        = string
  default     = "grocerymate"
}

variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t3.small"
}

variable "key_name" {
  description = "Existing EC2 key pair name."
  type        = string
  default     = "grocerymate-week2-key"
}

variable "allowed_ssh_cidr" {
  description = "Trusted client address for SSH access."
  type        = string
  default     = "0.0.0.0/32"
}

variable "allowed_app_cidr" {
  description = "Trusted client address for GroceryMate access."
  type        = string
  default     = "0.0.0.0/0"
}

variable "db_username" {
  description = "PostgreSQL administrator username."
  type        = string
  default     = "postgres"
}

variable "s3_bucket_name" {
  description = "Globally unique private S3 bucket name."
  type        = string

}

variable "owner" {
  description = "Owner tag applied to managed resources."
  type        = string
  default     = "Dr. Torsten Bernasco"
}

variable "db_name" {
  description = "PostgreSQL application database name."
  type        = string
  default     = "grocerymate_db"
}

variable "db_instance_class" {
  description = "RDS instance class."
  type        = string
  default     = "db.t4g.micro"
}

variable "db_allocated_storage" {
  description = "RDS allocated storage in GiB."
  type        = number
  default     = 20
}

variable "root_volume_size" {
  description = "EC2 root volume size in GiB."
  type        = number
  default     = 8
}

variable "backup_retention_days" {
  description = "RDS automated backup retention in days."
  type        = number
  default     = 7

  validation {
    condition = (
      var.backup_retention_days >= 1 &&
      var.backup_retention_days <= 35 &&
      floor(var.backup_retention_days) == var.backup_retention_days
    )
    error_message = "Backup retention must be a whole number from 1 to 35."
  }
}

variable "final_snapshot_identifier" {
  description = "Unique final snapshot name for a planned database deletion."
  type        = string
}

variable "repository_url" {
  description = "Public HTTPS Git repository used for application deployment."
  type        = string
  default     = "https://github.com/charlemagnevolt-hub/AWS_grocery.git"
}

variable "app_revision" {
  description = "Git commit SHA containing the runtime secret integration."
  type        = string

  validation {
    condition     = can(regex("^[0-9a-f]{40}$", var.app_revision))
    error_message = "Use a full 40-character Git commit SHA."
  }
}
