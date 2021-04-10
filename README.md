# uts-rp-autumn2021
UTS researchProject autumn2021 intrusionDetectionSystem

- Install apps
```bash
sudo apt update -y && sudo apt upgrade -y
sudo apt install git postgresql python3-pip libpq-dev python3.8-dev -y
```

- Configure postgres
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE ids;
\password postgres
\q
```

- Clone repo
```bash
cd ~
git clone https://github.com/sukanthm/uts-rp-autumn2021.git
```

- Add config files alongside their '_example' counterparts
	- ./private_config.py

- Install py dependencies
```bash
cd ~/uts-rp-autumn2021
sudo pip3 install -r ./requirements.txt
```

- Build DB
```bash
python3 ./build_db.py all
```