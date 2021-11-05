import uvicorn

# gunicorn app.app:app --bind 0.0.0.0:5000 -k uvicorn.workers.UvicornWorker
if __name__ == '__main__':
    uvicorn.run('dispimdb_api.app.app:app',
                host='0.0.0.0',
                port=5000,
                reload=True)
