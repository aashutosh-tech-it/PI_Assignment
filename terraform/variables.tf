variable "subscription_id" {}
variable "client_id" {}
variable "client_secret" {
  sensitive = true
}
variable "tenant_id" {}
variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {
    environment = "dev"
    owner       = "assignment"
  }
}
variable "location" {
  default = "westeurope"
}
variable "rg_name" {
  default = "rg-pi-devopstf-weu"
}
variable "aks_name" {
  default = "aks-pi-devopstf-weu"
}
variable "acr_name" {
  default = "acrpidevopstfweu01"
}
variable "kv_name" {
  default = "kv-pi-devopstf-weu"
}
variable "vnet_name" {
  default = "vnet-pi-devopstf-weu"
}
variable "subnet_name" {
  default = "snet-pi-aks-weu"
}
