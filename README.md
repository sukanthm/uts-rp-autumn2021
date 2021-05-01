# uts-rp-autumn2021
UTS researchProject autumn2021 intrusionDetectionSystem
<br/>

- Install apps
```bash
sudo apt update -y && sudo apt upgrade -y
sudo apt install git postgresql python3-pip libpq-dev python3.8-dev -y
```
<br/>

- Configure postgres
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE ids;
\password postgres
\q
```
<br/>

- Clone repo
```bash
cd ~
git clone https://github.com/sukanthm/uts-rp-autumn2021.git
```
<br/>

- Add config files alongside their '_example' counterparts
	- ./private_config.py

<br/>

- Install py dependencies
```bash
cd ~/uts-rp-autumn2021
sudo pip3 install -r ./requirements.txt
```
<br/>

- Build DB
```bash
python3 ./build_db.py all #wipe db (config + data)
python3 ./build_db.py data #wipe only data table
```
<br/>

- Populate config tables
```bash
python3 ./populate_db_config.py
```
<br/>

- RUN
```bash
#3 children
clear;clear;python3 build_db.py all && python3 populate_db_config.py && python3 ids.py 3
```

- Notes
```
All packets are checked against bad clusters first, then good clusters, only then becomes an anomaly. 
The anomaly is tagged to the first closest cluster (bad then good) based on its anomaly score (lower the better)


good, bad get score of 0
anomaly score range <- (0, 1]

anomaly score = 1 - (n_inDimensions/total_dimensions)

anomaly score of 1 implies fully outside the cluster
anomaly cant have score 0 as that means its fully inside a cluster and thus has to be good/bad
higher the anomaly score, the more outside the cluster it is
we pick the lowest anomaly for a packet score and send to sql (i.e. tagging the closest cluster)
```