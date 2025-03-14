output "fastapi_url" {
  value = "http://${azurerm_container_group.madebayofastapi.ip_address}:80"
  description = "Public URL of the FastAPI application"
}