# ds-order service
Distributed Systems, Fall 2023


## Migrate databse

python migrate.py

## Run Tests

python test.py

### Run service

```console
python -m flask run --host=0.0.0.0 --port=8081
```

## Public API

### GetOrderStatus

http://127.0.0.1:8081/order/<order_id>

Response

```json
[
    {
        "status": "",
       
    }
]
```

## Messaging

Console
https://el6icz3en0fo-scdyi8ws59yk.cedalo.dev/

MQTT Endpoint Address: mqtt://el6icz3en0fo-scdyi8ws59yk.cedalo.dev:1883

## Outgoing messages 

### OrderCanceled

topic: order/order-canceled

```json
{"orderId": ""}

```
## Incoming messages

### InStock

topic: inventory/on-stock

```json
{"orderId": ""}
```
### OutOfStock

topic: inventory/out-of-stock

```json
{"orderId": ""}
```

### Order send

topic: public-front/order-send

```json
{"orderId": "", "items": [{"inventoryId": 1, "count": 10}, {"inventoryId": 2, "count": 10}]}
```
### OrderCanceled

topic: public-front/order-canceled
```json
{"orderId": ""}
```
