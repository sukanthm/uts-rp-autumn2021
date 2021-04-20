#DB CONFIG TABLE DATA
clusters = [
    {'id': 1, 'cluster_type': 'G', 'cluster_name': '192.168.0.0/24 ssh only', 'cluster_description': 'allows ssh from 192.168.0.0/24',},
    {'id': 2, 'cluster_type': 'B', 'cluster_name': '192.168.0.0/24 ssh only', 'cluster_description': 'blocks p < shh from 192.168.0.0/24',},
    {'id': 3, 'cluster_type': 'B', 'cluster_name': '192.168.0.0/24 ssh only', 'cluster_description': 'blocks p > shh from 192.168.0.0/24',},

    {'id': 4, 'cluster_type': 'G', 'cluster_name': 'night small data only', 'cluster_description': '10pm to 7am let 10-500 size',},
    {'id': 5, 'cluster_type': 'B', 'cluster_name': 'night small data only', 'cluster_description': '10pm to 7am block 10,000-100,000 size',},
]
cluster_definitions = [
    {'cluster_id': 1, 'dimension': 'src_ip', 'range_start': '192.168.0.1', 'range_end': '192.168.0.255'},
    {'cluster_id': 1, 'dimension': 'dst_port', 'range_start': '22', 'range_end': '22'},
    {'cluster_id': 2, 'dimension': 'src_ip', 'range_start': '192.168.0.1', 'range_end': '192.168.0.255'},
    {'cluster_id': 2, 'dimension': 'dst_port', 'range_start': '1', 'range_end': '21'},
    {'cluster_id': 3, 'dimension': 'src_ip', 'range_start': '192.168.0.1', 'range_end': '192.168.0.255'},
    {'cluster_id': 3, 'dimension': 'dst_port', 'range_start': '23', 'range_end': '65535'},

    {'cluster_id': 4, 'dimension': 'time', 'range_start': '2200', 'range_end': '0700'},
    {'cluster_id': 4, 'dimension': 'msg_size', 'range_start': '10', 'range_end': '500'},
    {'cluster_id': 5, 'dimension': 'time', 'range_start': '2200', 'range_end': '0700'},
    {'cluster_id': 5, 'dimension': 'msg_size', 'range_start': '1000', 'range_end': '100000'},
]


#GENERATOR CONFIG 
#[value, weight]. '' for fully random
gen_ips = [
        ['192.168.0', 2],
        ['10.12', 2],
        ['1.1.1.1', 1],
        ['', 1],
    ]
gen_ports_dst = [
        ['22', 3], #ssh
        ['80', 1], #http
        ['5432', 1], #postgres default
    ]
gen_ports_src = [
        ['', 1],
    ]

generator_timeline = [
    #secs, job, items/sec
    [5, 'random', 5],
    [5, 'ddos', 20],
    [5, 'random', 5]
]
ddos_no_of_ip = 5

#IDS CONFIG
LIVE_FREQ_DDOS_THRESHOLD = 10 #ge items/sec
open_tcp_conn_THRESHOLD = 10 #ge current open tcp connections 