import psycopg2
import psycopg2.extras

from private_config import postgres_credentials
from public_config import clusters, cluster_definitions


def main():
    try:
        conn = psycopg2.connect(postgres_credentials)
        cur = conn.cursor()
    except Exception as e:
        print(datetime.now(TZ), "db conn/cur ERROR")
        logging.error(str(datetime.now(TZ)) + ' ' + traceback.format_exc())
        print(datetime.now(TZ), "END")
        return False

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