from init import app
import os

app.secret_key = os.environ.get('SECRET_KEY')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

