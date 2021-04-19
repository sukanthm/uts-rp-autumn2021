from datetime import datetime, timedelta
import random
import string
import time

from public_config import gen_ips as ips
from public_config import gen_ports_dst, gen_ports_src
from public_config import generator_timeline, ddos_no_of_ip


def ip_gen(ips):
    while True:
        ip = random.choices([i[0] for i in ips], 
            weights=[i[1] for i in ips])[0]
        if ip == '':
            ip += str(random.randint(1, 255))
        for i in range(3-ip.count('.')):
            ip += '.' + str(random.randint(1, 255))
        yield ip


def port_gen(ports):
    while True:
        port = random.choices([i[0] for i in ports], 
            weights=[i[1] for i in ports])[0]
        if port == '':
            port = str(random.randint(49152, 65535)) #ephemeral only
        yield port


def dummy_KVs_gen():
    while True:
        output = {}
        for i in range(random.randint(1, 4)):
            key = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))
            value = ''.join(random.choices(string.hexdigits, k=random.randint(0, 20)))
            output[key] = value
        yield output


def time_gen():
    today = datetime.now()
    while True:
        yield today.replace(
            hour=random.randint(0, 23), 
            minute=random.randint(0, 59), 
            second=random.randint(0, 59), 
            microsecond=0
        )


def main():
    for [secs, job, items_per_sec] in generator_timeline:

        if job == 'random':
            ip_gen_obj = ip_gen(ips)
            dst_port_gen_obj = port_gen(gen_ports_dst)
            src_port_gen_obj = port_gen(gen_ports_src)
            dummy_KVs_obj = dummy_KVs_gen()
            time_gen_obj = time_gen()

            sleep_secs = 1 / items_per_sec
            job_start = datetime.now()
            while job_start + timedelta(seconds=secs) >= datetime.now():
                time.sleep(sleep_secs)
                data = {
                    'src_ip': next(ip_gen_obj),
                    'src_port': next(src_port_gen_obj),
                    'dst_port': next(dst_port_gen_obj),
                    'datetime': next(time_gen_obj),
                    'msg_size': random.randint(10, 10**5),
                    **next(dummy_KVs_obj),
                }
                yield data
        

        if job == 'ddos':
            ip_gen_obj = ip_gen([['', 1]])
            IPs = [next(ip_gen_obj) for i in range(ddos_no_of_ip)] #pick N ip to ddos from
            src_port_gen_obj = port_gen(gen_ports_src) #fully random
            dummy_KVs_obj = dummy_KVs_gen()
            time_gen_obj = time_gen()

            sleep_secs = 1 / items_per_sec
            job_start = datetime.now()
            while job_start + timedelta(seconds=secs) >= datetime.now():
                time.sleep(sleep_secs)
                data = {
                    'src_ip': random.choice(IPs),
                    'src_port': next(src_port_gen_obj),
                    'dst_port': 443, #ddos always on https
                    'datetime': next(time_gen_obj),
                    'msg_size': random.randint(10, 10**5),
                    #client will never send final 'ACK', after theoretically receiving a 'SYN+ACK' from server
                    'TCP_FLAG': 'SYN',
                    **next(dummy_KVs_obj),
                }
                yield data


if __name__ == '__main__':
    main()