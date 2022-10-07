output "server_ips_public" {
  description = "Public IP addresses of instances"
  value       = aws_instance.main_node.*.public_ip
}

output "server_ips_private" {
  description = "Private IP addresses of instances"
  value       = aws_instance.main_node.*.private_ip
}

# output "proxy_ips_public" {
#   description = "Public IP addresses of instances"
#   value       = aws_instance.proxy_node.*.public_ip
# }

# output "proxy_ips_private" {
#   description = "Private IP addresses of instances"
#   value       = aws_instance.proxy_node.*.private_ip
# }