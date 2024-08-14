# -*- coding: utf-8 -*-
from datetime import datetime
from imio.scan_logger import CLIENTS_DIC
from imio.scan_logger import LOG_DIR
from imio.scan_logger.utils import send_notification
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service

import os
import re


class MessageReceiver(Service):
    def reply(self):
        data = json_body(self.request)
        client_id = data.get("client_id", None)
        message = data.get("message", None)
        level = data.get("level", "")

        if not client_id or not message:
            self.request.response.setStatus(400)
            return {"status": "error", "message": "client_id and message are required in json body"}
        if not re.match(r"^0\d{5}$", client_id):
            return {
                "status": "error",
                "message": "client_id must be 6 digits long, start with zero, and contain only digits.",
            }
        if client_id not in CLIENTS_DIC:
            send_notification(
                f"Unknown client {client_id} in scan_logger",
                [f"Cannot find {client_id} in clients dic: len is {len(CLIENTS_DIC)}"],
            )
        client_dir = os.path.join(LOG_DIR, client_id)
        os.makedirs(client_dir, exist_ok=True)
        file_path = os.path.join(client_dir, "messages.log")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Open the file in append mode and write the message with the timestamp
        with open(file_path, "a") as file:
            file.write(f"{current_time} {message}\n")

        if level == "ERROR":
            send_notification(f"Message from {client_id} - {CLIENTS_DIC.get(client_id)}", message.split("\n"))

        return {"status": "success", "message": "Log received"}
