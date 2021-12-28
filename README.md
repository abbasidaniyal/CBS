## Deployment Steps

### First time setup

1. Update system
```
sudo apt update && sudo apt upgrade
```

2. Install python, python-venv, postgresql (local database)
```
sudo apt install python3.9 python3.9-venv python3.9-dev postgresql nginx
```

3. Configure postgresql
Create user/password
```
sudo su postgres
psql
create user <USERNAME> with encrypted password '<PASSWORD>';
```

Create database
```
create database cbs-website-db
GRANT ALL PRIVILEGES ON DATABASE cbs-website-db TO <USERNAME>;
```

4. Make system user
```
sudo adduser website
su website
```

5. Make dir and clone code
```
mkdir website
git clone https://github.com/abbasidaniyal/CBS.git website
```

6. Create venv and install requirements
```
cd website
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

7. Setup secrets
```
cp .env_sample .env
```

Fill in the required values in .env file


8. Test run
```
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
gunicorn --bind 0.0.0.0:8000 cbs.wsgi
```

9. Create superadmin
```
python manage.py createsuperuser
```

10. Create deamon job
Switch to user with sudo permission

Create service file
```
cp deploy/website.service /etc/systemd/system/website.service

```
Start and enable website
```
sudo systemctl start website
sudo systemctl enable website
```

Check status
```sudo systemctl status gunicorn```

To see logs
```
sudo journalctl -u gunicorn
```

To propogate changes
```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

11. Setup nginx
Copy conf from deploy/nginx.conf and add to /etc/nginx/sites-available/website

Enable available site
```
sudo cp deploy/nginx.conf /etc/nginx/sites-available/website
sudo ln -s /etc/nginx/sites-available/website /etc/nginx/sites-enabled
```

Restart to propogate changes
```
sudo systemctl restart nginx
```

12. SSL encryption
Install python certbot
```
sudo apt-get install python3-certbot-nginx
```

Configure firewall
```
sudo ufw allow 'Nginx Full'
```

Set dns entries to the IP of the machine

Get certificate

```
sudo certbot --nginx -d connectbuild.com -d www.connectbuild.com
```
Note: Setup http to https redirect


## Updating code

1. Pull new code
```
su website
cd website
git pull origin master
```

2. Update requirements and run migrations 
```
pip install -r requirements.txt
python manage.py collectstatic  --noinput
python manage.py migrate  --noinput
```

3. Restart service 
```
sudo systemctl restart website.service
```