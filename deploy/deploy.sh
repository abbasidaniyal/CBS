echo ${KEY} > /tmp/deploy_rsa 
ssh -o "StrictHostKeyChecking=no" -i /tmp/deploy_rsa -A ${HOST_USER}@${HOST_IP} << EOT
cd /home/website/CBS
git pull origin master
source env/bin/activate
pip install -r requirements.txt
python manage.py collectstatic  --noinput
python manage.py migrate  --noinput
sudo service website restart
echo "Deploy Finished"
EOT