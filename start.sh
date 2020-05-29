nohup gunicorn -b 0.0.0.0:9000 watchlist:app  2>&1 &
/etc/init.d/nginx start
