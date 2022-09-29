output "server_ips_public" {
  description = "Public IP addresses of instances"
  value       = aws_instance.main.*.public_ip
}

output "server_ips_private" {
  description = "Private IP addresses of instances"
  value       = aws_instance.main.*.private_ip
}