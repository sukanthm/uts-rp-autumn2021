import psycopg2
import psycopg2.extras

from private_config import postgres_credentials

def main():
    try:
        conn = psycopg2.connect(postgres_credentials)
        cur = conn.cursor()
    except Exception as e:
        print(datetime.now(TZ), "db conn/cur ERROR")
        logging.error(str(datetime.now(TZ)) + ' ' + traceback.format_exc())
        print(datetime.now(TZ), "END")
        return False

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

    psycopg2.extras.execute_batch(cur,
    '''
        INSERT INTO clusters (id, cluster_type) 
        VALUES (%(id)s, %(cluster_type)s);
    ''', clusters)
    psycopg2.extras.execute_batch(cur,
    '''
        INSERT INTO cluster_definition (cluster_id, dimension, range_start, range_end) 
        VALUES (%(cluster_id)s, %(dimension)s, %(range_start)s, %(range_end)s);
    ''', cluster_definitions)

    conn.commit()
    cur.close()
    conn.close()
    print('config populated successfully')


if __name__ == '__main__':
    main()