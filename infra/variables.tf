variable "resource_group_name" {
  type        = string
  description = "Nome do Resource Group"
  default     = "rg-fiap-cp2-cloud-solutions"
}

variable "location" {
  type        = string
  description = "Região Azure"
  default     = "eastus2"
}

variable "mysql_location" {
  type        = string
  description = "Região do MySQL Flexible Server (pode diferir da região do Resource Group)"
  default     = "mexicocentral"
}

variable "mysql_admin_username" {
  type        = string
  description = "Administrador do MySQL Flexible Server"
  default     = "queimadasadmin"
}

variable "mysql_admin_password" {
  type        = string
  description = "Senha do admin do MySQL"
  sensitive   = true
}

variable "database_name" {
  type        = string
  description = "Nome do banco"
  default     = "queimadas"
}
