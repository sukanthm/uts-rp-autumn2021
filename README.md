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
python3 ./populate_config.py
```
<br/>

- RUN
```bash
python3 build_db.py all && python3 populate_config.py
python3 build_db.py data && python3 ids.py 3 #3 children
```