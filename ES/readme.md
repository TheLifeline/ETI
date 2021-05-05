# 第一次运行时注意事项

编辑 /etc/sysctl.conf，追加以下内容：
- vm.max_map_count=262144

保存后，执行：
- sysctl  -p
