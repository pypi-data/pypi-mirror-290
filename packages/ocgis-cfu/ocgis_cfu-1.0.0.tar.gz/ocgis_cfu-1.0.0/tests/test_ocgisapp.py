import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ocgis.ocgisapp import OcGisApp
import pylogfig
import time
from test_content import test_string
config = pylogfig.Config('tests\\config.toml')
config.load_logging_config(config.get('logging'))
app = OcGisApp(
    arcgis_username = config.get('arcgis.username'), 
    arcgis_password = config.get('arcgis.password'), 
    arcgis_link= config.get('arcgis.link'), 
    layer_url = config.get('arcgis.layer_url'), 
    onecall_username = config.get('onecall.username'), 
    onecall_password = config.get('onecall.password'), 
    onecall_login_url = config.get('onecall.login_url'), 
    districts = config.get('onecall.districts'), 
    update_range = config.get('settings.update_range'), 
    driver_executable_path = config.get('webdriver.driver_executable_path'), 
    closed_statuses = config.get('onecall.closed_statuses'), 
    state = "IA"
    )

#app.run()
#exit()
while(True):
    app.run()
