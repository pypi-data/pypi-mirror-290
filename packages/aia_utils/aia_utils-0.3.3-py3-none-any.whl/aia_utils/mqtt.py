from aia_utils.logs_cfg import config_logger
import paho.mqtt.client as paho
from dotenv import load_dotenv
import os
from aia_utils.toml_utils import aia_utils_version
__version__ = aia_utils_version()
import logging
load_dotenv()

# https://www.hivemq.com/demos/websocket-client/

class MqttClient:
    def __init__(self, topic: str, client_id: str):
        config_logger()
        self.logger = logging.getLogger(__name__)
        self.host = os.environ['MQTT_HOST']
        self.port = os.environ['MQTT_PORT']
        self.username = os.environ['MQTT_USERNAME']
        self.password = os.environ['MQTT_PASSWORD']
        self.client_id = client_id
        self.topic = topic
        self.client = paho.Client(paho.CallbackAPIVersion.VERSION2, client_id=client_id, clean_session=True, userdata=None, protocol=paho.MQTTv31)
        #self.client.will_set(topic, payload=None, qos=0, retain=False)
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.host, keepalive=60, bind_address="")
        self.client.loop_start()
        self.logger.info(f"Listener MqttClient Ready v{__version__}")
        #self.client.loop_forever()
    
    def send_message(self, message: str):
        msg_info = self.client.publish(self.topic, message, qos=1)
        #if msg_info.is_published() == False:
        #    print('Message is not yet published.')
        msg_info.wait_for_publish()
        self.logger.debug(f"Message sent: {message}")