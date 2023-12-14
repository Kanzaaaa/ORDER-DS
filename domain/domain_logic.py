from domain.orders import Orders
from typing import List
import sqlite3
from sqlite3 import Error
from domain.order import OrderOut, OrderInStock, OrderCancel
import config
from domain.messages import order_canceled
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def GetOrderStatus(order_id: str) -> str:
    conn = create_connection(config.db)
    order_status = "Order not found"  

    if conn:
        try:
            cursor = conn.execute('SELECT order_status FROM "order" WHERE order_id = ?;', (order_id,))
            row = cursor.fetchone()
            if row:
                order_status = row[0]
            print(f"Order fetch executed {order_id}")
        finally:
            conn.close()

    return '{"order_status": "' + order_status + '"}'


def OrderSend(order: Orders):
    # Insert the order into the database with status "unknown"
    insert_order(order.order_id, "unknown")

def outstock(order_out: OrderOut):
    # Process the out-of-stock event and update the order status to unsuccessful
    update_order_status(order_out.order_id, "unsuccessful")

def onstock(order_in_stock: OrderInStock):
    # Process the in-stock event and update the order status to successful
    update_order_status(order_in_stock.order_id, "successful")

def order_cancel(order_cancel: OrderCancel):
        update_order_status(order_cancel.order_id, "canceled")
        message_publish(config.mqtt_topic_on_order_canceled_2, order_canceled(order_cancel.order_id).to_json())

def insert_order(order_id, order_status):
    # Check if the order with the given ID already exists
    if not order_exists(order_id):
        # If no rows are found, insert a new record into the "order" table
        conn = create_connection(config.db)

        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO "order" (order_id, order_status) VALUES (?, ?)', (order_id, order_status))
                conn.commit()
            except Error as e:
                print(e)
            finally:
                conn.close()
    else:
        print(f"Order with ID {order_id} already exists. No new row inserted.")

def order_exists(order_id):
    # Check if an order with the given ID exists in the "order" table
    conn = create_connection(config.db)

    if conn is not None:
        try:
            cursor = conn.execute('SELECT 1 FROM "order" WHERE order_id = ? LIMIT 1', (order_id,))
            row = cursor.fetchone()
            return row is not None
        except Error as e:
            print(e)
        finally:
            conn.close()

    return False


def update_order_status(order_id, new_status):
    # Update the order status in the database
    conn = create_connection(config.db)

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE "order" SET order_status = ? WHERE order_id = ?', (new_status, order_id))
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

def message_publish(topic: str, payload: str):
    print("")
    print("\033[93mOutgoing message\033[00m")
    print(F"\033[93mTopic: {topic}\033[00m")
    print(F"\033[93mPayload: {payload}\033[00m")

    publish.single(
        topic,
        payload=payload,
        qos=1,  # least once
        retain=False,
        hostname=config.mqtt_host,
        port=config.mqtt_port,
        client_id=config.mqtt_client_id,
        auth={'username': config.mqtt_username, 'password': config.mqtt_password},
        tls=None,
        protocol=mqtt.MQTTv5, transport=config.mqtt_transport)
