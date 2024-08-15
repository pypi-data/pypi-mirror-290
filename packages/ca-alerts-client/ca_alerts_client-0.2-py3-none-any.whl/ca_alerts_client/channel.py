import json
import tempfile
import base64
import uuid
from datetime import datetime

import pika
from pandas import DataFrame
import dataframe_image as dtf

from .abs_channel import AbstractChannel
from .helpers import get_exception_text, get_current_file_name


class TelegramChannel(AbstractChannel):
    MAX_TIMEOUT = 60

    def __init__(
            self,
            project: str,
            rmq_host: str,
            rmq_user: str,
            rmq_password: str,
            severity: str
    ) -> None:
        self.project = project
        self.severity = severity
        try:
            credentials = pika.PlainCredentials(rmq_user, rmq_password)
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=rmq_host, credentials=credentials, socket_timeout=5)
            )
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange='main', exchange_type='topic', durable=True)
        except Exception as e:
            print(e)

    def send_message(self, message: str) -> None:
        caption = self._prepare_caption(message)
        data = {
            "type": "text",
            "text": caption,
            "project": self.project,
            "severity": self.severity
        }
        self._send_to_rmq(data)

    def send_as_xmlx(self, df: DataFrame, caption: str = ""):
        with tempfile.NamedTemporaryFile(delete=True, suffix=".xlsx") as temp_file:
            df.to_excel(temp_file.name, index=False)
            temp_file.seek(0)
            content = temp_file.read()
            if not content:
                raise ValueError("DF пуст")
            base64_encoded = base64.b64encode(content).decode('utf-8')
            caption = self._prepare_caption(caption)
            data = {
                "type": "file",
                "text": caption,
                "project": self.project,
                "severity": self.severity,
                "file": base64_encoded,
                "filename": f"{uuid.uuid4()}.xlsx"
            }
            self._send_to_rmq(data)

    def send_as_png(self, df: DataFrame, caption: str = ""):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            dtf.export(
                df,
                filename=temp_file.name,
                table_conversion='matplotlib'
            )
            temp_file.seek(0)
            content = temp_file.read()
            if not content:
                raise ValueError("DF пуст")
            base64_encoded = base64.b64encode(content).decode('utf-8')
            caption = self._prepare_caption(caption)
            data = {
                "type": "photo",
                "text": caption,
                "project": self.project,
                "severity": self.severity,
                "file": base64_encoded,
            }
            self._send_to_rmq(data)

    def send_exception(self, e: Exception, caption: str = "") -> None:
        exception_text = get_exception_text(e)
        if caption:
            full_text = "📝 " + caption + "\n" + exception_text
        else:
            full_text = exception_text
        self.send_message(full_text)

    def _send_to_rmq(self, data: dict):
        self.channel.basic_publish(
            exchange='main', routing_key="", body=json.dumps(data), properties=pika.BasicProperties(
                content_type='application/json',
                delivery_mode=pika.DeliveryMode.Persistent,
            ))

    @staticmethod
    def _prepare_caption(caption: str):
        now = datetime.now()
        file_name = get_current_file_name()
        return (f"🕐 {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"📂 file {file_name}\n"
                f"{caption}")
