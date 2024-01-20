from pathlib import Path
import os

PERIOD_ROS_SPIN = 0.01
REGISTRATION_TIMEOUT = 5.0
SERVER_TIMEOUT = 5.0
GET_SERVER_INFO_TIMEOUT = 0.5
PATH_DATA_FOLDER = os.getenv('RAYA_APPS_DATA')
PATH_RESOURCES_FOLDER = Path('res')
SERVER_APP_NAMES = ['_ggs']
MAIN_SERVER_APP = '_ggs'
ROS_APPS_NAMESPACE = '/raya/apps'
DEFAULT_COMMAND_TIMEOUT = 2.0
CANCELATION_TIMEOUT = 2.0
CONTROLLER_INIT_TIMEOUT = 10.0
CONTROLLER_INIT_WAIT_PERIOD = 0.1
CONTROLLER_INIT_TIMEOUT_TICKS = int(
    (CONTROLLER_INIT_TIMEOUT / CONTROLLER_INIT_WAIT_PERIOD))
CONTROLLER_WAIT_PERIOD = 0.02
LISTENER_SENSOR_DEBOUNCE_TIME = 1.0
ROBOT_ID = 'ROBOT_ID'
CLIENT_ID = 'CLIENT_ID'
ALLOWED_AUDIO_FORMATS = ['.wav', '.mp3']
GLOBAL_APP_ID = ''
