mqtt_host = ''
mqtt_port = ''
mqtt_transport = 'tcp' #tcp or websockets. Use websockets if issues with firewall
mqtt_client_id = 'ds-inventory'
mqtt_username = 'ds-inventory'
mqtt_password = ''

mqtt_topic_on_stock = 'inventory/on-stock'
mqtt_topic_out_of_stock = 'inventory/out-of-stock'
mqtt_topic_on_order_send = 'public-front/order-send'

mqtt_topic_on_order_canceled = 'public-front/order-canceled'
mqtt_topic_on_order_canceled_2 = 'order/order-canceled'

db = './db/ds-order.sqlite'
db_migrate = './migrate_scripts/*.sql'