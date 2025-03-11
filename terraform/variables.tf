variable "resource_group_name" {
  description = "Name of the existing Azure Resource Group"
  type        = string
}

variable "container_registry_name" {
  description = "Name of the existing Azure Container Registry"
  type        = string
}

variable "fastapi_container_name" {
  description = "Name of the FastAPI container"
  type        = string
  default     = "madebayofastapi"
}

variable "fastapi_image" {
  description = "Docker image for FastAPI"
  type        = string
}

variable "cpu" {
  description = "CPU allocation for container"
  type        = number
  default     = 1
}

variable "memory" {
  description = "Memory allocation for container"
  type        = number
  default     = 4
}
