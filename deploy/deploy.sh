ssh -o "StrictHostKeyChecking=no" -i /tmp/deploy.cer  -A ${HOST_USER}@${HOST_IP} << EOT
cd /home/website/CBS
sudo git stash
sudo git pull origin master
source env/bin/activate
pip install -r requirements.txt
python manage.py collectstatic  --noinput
python manage.py migrate  --noinput
sudo service website restart
echo "Deploy Finished"
EOT
