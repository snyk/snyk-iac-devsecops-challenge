module "validate_ip" {
  source  = "github.com/p15r/terraform-validate-ip"
  ip_addr = "10.0.1.132"
}

output "is_valid" {
  value = module.validate_ip.result
}
