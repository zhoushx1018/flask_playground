nohup gunicorn -b 0.0.0.0:1317 watchlist:app --log-level=debug 2>&1 &
