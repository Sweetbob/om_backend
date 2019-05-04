import pexpect


def is_alive(ip):
    # todo 只有linux才能ping
    try:
        ping = pexpect.spawn('ping -c 1 %s' % ip)
        check = ping.expect([pexpect.TIMEOUT,"1 packets transmitted, 1 received, 0% packet loss"], 2)  # 2代表超时时间
        if check == 0:
            return False
        if check == 1:
            return True
    except Exception:
        return False
