import paramiko

private_key = paramiko.RSAKey.from_private_key_file('C:/Users/lool/Desktop/id_rsa')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.31.142', port=22, username='root', pkey=private_key)
stdin, stdout, stderr =ssh.exec_command('ifconfig')
result = stdout.read()
print(result.decode())
ssh.close()
