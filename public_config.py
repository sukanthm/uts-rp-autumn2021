#DB CONFIG
clusters = [
    {'id': 1, 'cluster_type': 'G'}, #clusters 1-3 allow only ssh from network 192.168.0.0/24
    {'id': 2, 'cluster_type': 'B'},
    {'id': 3, 'cluster_type': 'B'},
]
cluster_definitions = [
    {'cluster_id': 1, 'dimension': 'src_ip', 'range_start': '192.168.0.1', 'range_end': '192.168.0.255'},
    {'cluster_id': 1, 'dimension': 'dst_port', 'range_start': '22', 'range_end': '22'},
    {'cluster_id': 2, 'dimension': 'src_ip', 'range_start': '192.168.0.1', 'range_end': '192.168.0.255'},
    {'cluster_id': 2, 'dimension': 'dst_port', 'range_start': '1', 'range_end': '21'},
    {'cluster_id': 3, 'dimension': 'src_ip', 'range_start': '192.168.0.1', 'range_end': '192.168.0.255'},
    {'cluster_id': 3, 'dimension': 'dst_port', 'range_start': '23', 'range_end': '65535'},
]


#GENERATOR CONFIG 
#[value, weight]. '' for fully random
gen_ips = [
        ['192.168.0', 2],
        ['10.12', 2],
        ['1.1.1.1', 1],
        ['', 1],
    ]
gen_ports = [
        ['22', 3],
        ['443', 1],
        ['', 1],
    ]