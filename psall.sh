ps -ef | grep flask
ps -ef | grep gunicorn
ps -ef | grep nginx

echo -------------------------
netstat -anp | grep nginx | grep -v unix
