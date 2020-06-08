#flask run -h 0.0.0.0  -p 8080
gunicorn -b 0.0.0.0:8080 watchlist:app --log-level=debug