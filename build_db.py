from datetime import datetime
import logging
import pytz
import sys
import traceback

import psycopg2

from private_config import postgres_credentials

TZ = pytz.timezone('Australia/Sydney')


def main():
    print(datetime.now(TZ), "START")

    if len(sys.argv) != 2:
        print(datetime.now(TZ), 'bad number of script args, exiting')
        print(datetime.now(TZ), "END")
        return False
    
    command = sys.argv[1]
    if command not in ['all', 'data']:
        print(datetime.now(TZ), 'bad script arg, exiting')
        print(datetime.now(TZ), "END")
        return False
    else:
        try:
            conn = psycopg2.connect(postgres_credentials)
            cur = conn.cursor()
        except Exception as e:
            print(datetime.now(TZ), "db conn/cur ERROR")
            logging.error(str(datetime.now(TZ)) + ' ' + traceback.format_exc())
            print(datetime.now(TZ), "END")
            return False

        if command in ['all']:
            cur.execute('''
                DROP TABLE IF EXISTS clusters CASCADE;
                CREATE TABLE clusters (
                    id INTEGER,
                    cluster_type CHAR(1) NOT NULL,
                    cluster_name TEXT,
                    cluster_description TEXT,

                    PRIMARY KEY (id),
                    CONSTRAINT valid_cluster_type CHECK(cluster_type IN ('G', 'B'))
                );
                
                DROP TABLE IF EXISTS cluster_definition;
                CREATE TABLE cluster_definition (
                    cluster_id INTEGER,
                    dimension TEXT NOT NULL,
                    range_start TEXT NOT NULL,
                    range_end TEXT NOT NULL,

                    CONSTRAINT fk_cluster_id1 FOREIGN KEY(cluster_id) REFERENCES clusters(id)
                );
            ''')
            print(datetime.now(TZ), "rebuilt clusters, cluster_definition tables")

        if command in ['all', 'data']: #fk constraint drop is bad
            cur.execute('''
                CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
                DROP TABLE IF EXISTS data;
                CREATE TABLE data (
                    id uuid DEFAULT uuid_generate_v4 (),
                    msg TEXT NOT NULL,
                    status TEXT NOT NULL,
                    score REAL,
                    datetime TIMESTAMPTZ NOT NULL,
                    cluster_id INTEGER,
                    child_id TEXT NOT NULL,

                    PRIMARY KEY (id)
                    --CONSTRAINT valid_status CHECK(status IN ('G', 'B', 'A', 'D'))
                    --CONSTRAINT fk_cluster_id2 FOREIGN KEY(cluster_id) REFERENCES clusters(id)
                );
            ''')
            print(datetime.now(TZ), "rebuilt data table")

        conn.commit()
        cur.close()
        conn.close()
        print(datetime.now(TZ), "STOP")
        return True


if __name__ == '__main__':
    main()