import json
import random
import string
import time

from public_config import gen_ips as ips
from public_config import gen_ports as ports


def ip_gen():
    while True:
        ip = random.choices([i[0] for i in ips], 
            weights=[i[1] for i in ips])[0]
        if ip == '':
            ip += str(random.randrange(1, 255))
        for i in range(3-ip.count('.')):
            ip += '.' + str(random.randrange(1, 255))
        yield ip


def port_gen():
    while True:
        port = random.choices([i[0] for i in ports], 
            weights=[i[1] for i in ports])[0]
        if port == '':
            port = str(random.randrange(1, 65535))
        yield port


def dummy_KVs():
    while True:
        output = {}
        for i in range(random.randrange(1, 4)):
            key = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randrange(1, 10)))
            value = ''.join(random.choices(string.hexdigits, k=random.randrange(0, 20)))
            output[key] = value
        yield output


def main():
    ip_gen_obj = ip_gen()
    port_gen_obj = port_gen()
    dummy_KVs_obj = dummy_KVs()
    while True:
        data = {
            'src_ip': next(ip_gen_obj),
            'dst_port': next(port_gen_obj),
            'msg_size': 0, #random.randrange(1, 10**5),
            **next(dummy_KVs_obj),
        }
        data['msg_size'] = len(json.dumps(data))
        print(data) #DEV
        time.sleep(1) #DEV
        # yield data #PROD


if __name__ == '__main__':
    main()