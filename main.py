from app import create_app
from config import config_by_name
import os

config_name = os.getenv('FLASK_CONFIG') or 'dev'
app = create_app()
app.config.from_object(config_by_name[config_name])

if __name__ == '__main__':
    app.run(debug=config_by_name[config_name].DEBUG)