from api import app
from utils.database_utilities import create_database, create_table

if __name__ == '__main__':
    create_table()
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)