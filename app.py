from flask import Flask
from flask_mqtt import Mqtt
import domain.domain_logic as dl
import config
from domain.order import Order,OrderOut,OrderInStock,OrderCancel

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = config.mqtt_host  
app.config['MQTT_BROKER_PORT'] = config.mqtt_port  
app.config['MQTT_USERNAME'] = config.mqtt_username  
app.config['MQTT_PASSWORD'] = config.mqtt_password 
app.config['MQTT_KEEPALIVE'] = 60  
app.config['MQTT_TLS_ENABLED'] = False  

mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("flask mqtt connected")
    mqtt.subscribe(config.mqtt_topic_on_order_send, qos=1)
    mqtt.subscribe(config.mqtt_topic_out_of_stock, qos=1)
    mqtt.subscribe(config.mqtt_topic_on_stock, qos=1)
    mqtt.subscribe(config.mqtt_topic_on_order_canceled, qos=1)



@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )

    if data['topic'] == config.mqtt_topic_on_order_send:
        print(data['payload'])
        dl.OrderSend(Order.from_json(data['payload']))
    elif data['topic'] == config.mqtt_topic_out_of_stock:
        print(data['payload'])
        dl.outstock(OrderOut.from_json(data['payload']))
    elif data['topic'] == config.mqtt_topic_on_stock:
        print(data['payload'])
        dl.onstock(OrderInStock.from_json(data['payload']))
    elif data['topic'] == config.mqtt_topic_on_order_canceled:
        print(data['payload'])
        dl.order_cancel(OrderCancel.from_json(data['payload']))


@app.route("/get_order_status/<order_id>")
def GetOrderStatus(order_id):
    return dl.GetOrderStatus(order_id)
