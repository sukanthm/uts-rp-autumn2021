from datetime import datetime
import multiprocessing
import json
import logging
import pytz
import random
import sys
import time
import traceback

import psycopg2
import psycopg2.extras

from generator import main as data_gen
from private_config import postgres_credentials

TZ = pytz.timezone('Australia/Sydney')

def get_clusters():
    try:
        conn = psycopg2.connect(postgres_credentials)
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    except Exception as e:
        print(datetime.now(TZ), "db conn/cur ERROR")
        logging.error(str(datetime.now(TZ)) + ' ' + traceback.format_exc())
        print(datetime.now(TZ), "END")
        return False

    dict_cur.execute(
    '''
        SELECT a.id, a.cluster_type, b.dimension, b.range_start, b.range_end 
        FROM clusters a JOIN cluster_definition b ON a.id=b.cluster_id;
    ''')
    clusters = dict_cur.fetchall()
    dict_cur.close()
    conn.close()
    return clusters


def process_data(data, clusters):
    #TODO: add dimension based anomaly checks
    time.sleep(0.1) #to stop DB flooding


def child(child_id, n_CHILDREN, clusters):
    child_id_text = f'child#{child_id}'
    print(datetime.now(TZ), f"{child_id_text} START")
    try:
        conn = psycopg2.connect(postgres_credentials)
        cur = conn.cursor()
    except Exception as e:
        print(datetime.now(TZ), "db conn/cur ERROR")
        logging.error(str(datetime.now(TZ)) + ' ' + traceback.format_exc())
        print(datetime.now(TZ), "END")
        return False

    data_gen_obj = data_gen()
    output = []
    timer_start = datetime.now(TZ)
    while True:
        data = next(data_gen_obj)

        metrics = process_data(data, clusters)

        data['datetime'] = str(data['datetime'])
        output.append({
            'msg': json.dumps(data),
            'status': 'A',
            'score': 42,
            'datetime': datetime.now(TZ),
            'cluster_id': 1,
            'child_id': child_id,
        })

        if (datetime.now(TZ) - timer_start).seconds > n_CHILDREN*3 + child_id:
            timer_end = datetime.now(TZ)
            ips = round(len(output)/(timer_end-timer_start).total_seconds(), 2) #items per second
            print(datetime.now(TZ), child_id_text, f'{ips} items/second, dumping to SQL')
            psycopg2.extras.execute_batch(cur,'''
                INSERT INTO data (msg, status, score, datetime, cluster_id, child_id) 
                VALUES (%(msg)s, %(status)s, %(score)s, %(datetime)s, %(cluster_id)s, %(child_id)s);
            ''', output)
            output = []
            conn.commit()
            timer_start = datetime.now(TZ)
    
    cur.close()
    conn.close()


def main():
    print(datetime.now(TZ), "parent START")
    if len(sys.argv) != 2:
        print(datetime.now(TZ), 'bad number of script args, exiting')
        print(datetime.now(TZ), "END")
        return False
    n_CHILDREN = int(sys.argv[1])

    clusters = get_clusters()

    start_dt = datetime.now(TZ)
    print(datetime.now(TZ), f'starting {n_CHILDREN} children, children will dump data every {n_CHILDREN*3} secs')
    for i in range(n_CHILDREN):
        multiprocessing.Process(target=child, args=(i+1, n_CHILDREN, clusters)).start()        


if __name__ == '__main__':
    main()