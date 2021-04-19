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

    output = {'G': {}, 'B': {}} #cluster_id: [{cluster_definition...}, ...]
    for cluster in clusters:
        if cluster['id'] not in output[cluster['cluster_type']]:
            output[cluster['cluster_type']][cluster['id']] = []
        output[cluster['cluster_type']][cluster['id']].append({
            'dimension': cluster['dimension'],
            'range_start': cluster['range_start'],
            'range_end': cluster['range_end'],
        })

    return output


def compute_cluster_metrics(data, cluster_rules):
    in_counter = 0
    in_flag = True
    dimension_to_data_keyMap = {'time': 'datetime'}

    for rule in cluster_rules:
        data_key = dimension_to_data_keyMap.get(rule['dimension']) or rule['dimension']
        VALUE = data[data_key]

        if rule['dimension'] in ['dst_port', 'msg_size']:
            start, end = int(rule['range_start']), int(rule['range_end'])
            VALUE = int(VALUE)
        elif rule['dimension'] == 'time':
            start = datetime.strptime(rule['range_start'], '%H%M').time()
            end = datetime.strptime(rule['range_end'], '%H%M').time()
            VALUE = VALUE.time()
        else:
            start, end = rule['range_start'], rule['range_end']

        if start <= VALUE <= end:
            in_counter += 1
        else:
            in_flag = False

    return {
        'in?': in_flag,
        'score': 1 - round(in_counter/len(cluster_rules), 2),
    }


def process_data(data, clusters):
    #unconstrained ~4.5K ips/child
    min_score = 1.1 #real max score is 1 #TODO: improve this scoring system?
    best_cluster_metrics = None

    for cluster_id in clusters['B'].keys():
        cluster_output = compute_cluster_metrics(data, clusters['B'][cluster_id])
        if cluster_output['in?']:
            return {**cluster_output, 'status': 'B', 'cluster_id': cluster_id}
        elif cluster_output['score'] < min_score:
            min_score = cluster_output['score']
            best_cluster_metrics = {**cluster_output, 'cluster_id': cluster_id}

    for cluster_id in clusters['G'].keys():
        cluster_output = compute_cluster_metrics(data, clusters['G'][cluster_id])
        if cluster_output['in?']:
            return {**cluster_output, 'status': 'G', 'cluster_id': cluster_id}
        elif cluster_output['score'] < min_score:
            min_score = cluster_output['score']
            best_cluster_metrics = {**cluster_output, 'cluster_id': cluster_id}

    return {**best_cluster_metrics, 'status': 'A'}



def child(child_id, n_CHILDREN, clusters, db_dump_flag):
    time.sleep(child_id-1) #one time, to stagger DB dumps
    child_id_text = f'child#{child_id}'
    db_dump_gap = n_CHILDREN
    print() if child_id == 1 else False
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
    IDS_CONTINUE = True
    while IDS_CONTINUE:
        try:
            data = next(data_gen_obj)
            metrics = process_data(data, clusters)

            data['datetime'] = str(data['datetime'])
            output.append({
                'msg': json.dumps(data),
                'status': metrics.get('status'),
                'score': metrics.get('score'),
                'datetime': datetime.now(TZ),
                'cluster_id': metrics.get('cluster_id'),
                'child_id': child_id,
            })
        except StopIteration:
            IDS_CONTINUE = False

        if (not IDS_CONTINUE and len(output)) or (datetime.now(TZ) - timer_start).seconds > db_dump_gap:
            timer_end = datetime.now(TZ)
            ips = round(len(output)/(timer_end-timer_start).total_seconds(), 2) #items per second
            print() if child_id == 1 else False
            print(datetime.now(TZ), child_id_text, f'{ips} items/second, dumping {len(output)} items')
            if db_dump_flag:
                psycopg2.extras.execute_batch(cur,'''
                    INSERT INTO data (msg, status, score, datetime, cluster_id, child_id) 
                    VALUES (%(msg)s, %(status)s, %(score)s, %(datetime)s, %(cluster_id)s, %(child_id)s);
                ''', output)
                conn.commit()
            output = []
            timer_start = datetime.now(TZ)
    
    cur.close()
    conn.close()
    print(datetime.now(TZ), f"{child_id_text} STOP")
    return


def main():
    print(datetime.now(TZ), "parent START")
    if len(sys.argv) != 2:
        print(datetime.now(TZ), 'bad number of script args, exiting')
        print(datetime.now(TZ), "END")
        return False
    n_CHILDREN = int(sys.argv[1])

    clusters = get_clusters()

    start_dt = datetime.now(TZ)
    print(datetime.now(TZ), f'parent starting {n_CHILDREN} children')

    children = []
    for i in range(n_CHILDREN):
        children.append(
            multiprocessing.Process(target=child, args=(i+1, n_CHILDREN, clusters, False))
        )
        children[-1].start()
    
    for i in range(n_CHILDREN):
        children[i].join()
        print(datetime.now(TZ), f'parent JOINED child {i+1}')
    
    print()
    print(datetime.now(TZ), f'parent STOP')
    return


if __name__ == '__main__':
    main()