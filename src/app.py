from init import app
import os

secret_key = os.urandom(24)

app.secret_key = secret_key

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)