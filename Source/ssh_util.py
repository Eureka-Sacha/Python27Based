# -*- coding: utf-8 -*-
__author__ = '奎'

import paramiko


class SSHClient:
    def __init__(self, config):
        self.ip = config['ip']
        self.port = config['port']
        self.user = config['user']
        self.pwd = config['pwd']
        self.sshClient = paramiko.SSHClient()

    def start(self):
        self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshClient.connect(self.ip, self.port, self.user, self.pwd)
        pass

    def stop(self):
        self.sshClient.close()
        pass

    def exec_command(self, command):
        return self.sshClient.exec_command(command)


if __name__ == '__main__':
    config = {
        'ip': '192.168.31.57',
        'port': 22,
        'user': 'eureka',
        'pwd': '1234'
    }
    the_word = 'python'
    client = SSHClient(config)
    client.start()
    print 'client connected...'
    client.exec_command('python /home/eureka/hello.py')
    print 'run py'
    stdin, stdout, stderr = client.exec_command('docker ps |grep ' + the_word + '|awk \'{print $1}\'')
    id = stdout.readlines()[0]
    print 'find id' + id
    client.exec_command("docker cp temp.txt " + id + ":/home/temp2.txt")
    client.stop()
    print 'client closed...'
