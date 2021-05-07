from importlib import reload
import sys
from routes.app import create_app
from config import app_config, app_active

config = app_config[app_active]
config.APP = create_app(app_active)

if __name__ == '__main__':
    #config.IP_HOST
    #config.PORT_HOST
    config.APP.run(host=0.0.0.0, port=config.PORT_HOST=8000)
    reload(sys)
