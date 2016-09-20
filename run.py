import os
from cert_store import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(port=port)