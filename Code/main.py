from flask import request
from website import create_app

app = create_app()


@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, POST, OPTIONS, PUT, DELETE')
    return response


if __name__ == '__main__':
    app.run(debug=True)
