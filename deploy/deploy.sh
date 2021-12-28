#! /bin/bash

source env/bin/activate
echo "Installing requirements"
pip install -r requirements.txt
python manage.py collectstatic  --noinput
echo "Migrating database"
python manage.py migrate  --noinput
sudo service website restart
echo "Deploy Finished"
