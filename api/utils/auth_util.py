import os, sys, pexpect

from api.models import User


def check_login(token):
    """
    根据token验证用户
    """
    user = User.objects.filter(token=token).first()
    if user:
        return True
    return False


class SshCopy:

    def __init__(self, user, host, passwd, port):
        self.pub_key = os.getenv('HOME') + '/.ssh/id_rsa.pub'
        self.user = user
        self.host = host
        self.passwd = passwd
        self.port = port

    def send(self):
        str_ssh = '/usr/bin/ssh-copy-id -i %s %s@%s -p %s' % (self.pub_key, self.user, self.host, self.port)
        child = pexpect.spawn(str_ssh)
        try:
            index = child.expect(['continue connecting \(yes/no\)', '\'s password:', pexpect.EOF], timeout=20)
            print(index)
            if index == 0:
                child.sendline('yes')
                print(child.after, child.before)
            if index == 1:
                child.sendline(self.passwd)
                child.expect('password:')
                child.sendline(self.passwd)
                print(child.after, child.before)
            if index == 2:
                print('[ failed ]')
                print(child.after, child.before)
                child.close()
                return 'not'
        except Exception as e:
            print(child.after, child.before)
            child.close()
        else:
            print
            'nada feito'
