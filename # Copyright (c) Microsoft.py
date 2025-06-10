# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import asyncio
import random
import uuid

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
#   Run 'pip install azure-iot-device' to install the required libraries for this application
#   Note: Requires Python 3.6+

# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

# The device connection string to authenticate the device with your IoT hub.
CONNECTION_STRING = "HostName=MISSAO-05.azure-devices.net;DeviceId=microatividade_02;SharedAccessKey=Q2hOr0OmW6sXK13TBCGE3eEBGp+eDFxSYrWeEFO5q/0="

MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = "{\"temperature\": %.2f,\"humidity\": %.2f}"

# Temperature threshold for alerting
TEMP_ALERT_THRESHOLD = 30


async def main():
    try:
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        await client.connect()

        print("IoT Hub device sending periodic messages, press Ctrl-C to exit")

        while True:
            # Build the message with simulated telemetry values.
            temperature = TEMPERATURE + (random.random() * 15)
            humidity = HUMIDITY + (random.random() * 20)
            msg_txt_formatted = MSG_TXT % (temperature, humidity)
            message = Message(msg_txt_formatted)

            # Add standard message properties
            message_payload = {
            "body": {
                "messageId": 18,
                "deviceId": "Raspberry Pi Web Client",
                "temperature": 27.796111770668457,
                "humidity": 66.77637926438427
            },
            "applicationProperties": {
                "temperatureAlert": temperature_alert
            }}

            message_json = json.dumps(message_payload)
            message = Message(message_json)

            message.message_id = uuid.uuid4()
            message.content_encoding = "utf-8"
            message.content_type = "application/json"

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            prop_map = message.custom_properties
            prop_map["temperatureAlert"] = ("true" if temperature > TEMP_ALERT_THRESHOLD else "false")

            # Send the message.
            print("Sending message: %s" % message.data)
            try:
                await client.send_message(message)
            except Exception as ex:
                print("Error sending message from device: {}".format(ex))
            await asyncio.sleep(1)

    except Exception as iothub_error:
        print("Unexpected error %s from IoTHub" % iothub_error)
        return
    except asyncio.CancelledError:
        await client.shutdown()
        print('Shutting down device client')

if __name__ == '__main__':
    print("IoT Hub simulated device")
    print("Press Ctrl-C to exit")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Keyboard Interrupt - sample stopped')
