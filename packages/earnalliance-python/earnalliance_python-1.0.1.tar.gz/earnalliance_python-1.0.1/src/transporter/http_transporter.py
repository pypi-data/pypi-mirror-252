import asyncio as io
import hashlib
import hmac
import json
import time

import requests
from model.payload import Payload
from options import NodeOptions
from model.execution_result import (
    ExecutionResult,
    error_result,
    exception_result,
    success_result,
)
from utils import Scheduler as sc


class HTTPTransporter:
    def __init__(self, options: NodeOptions):
        self.options = options
        self.max_retry_attempts = options.maxRetryAttempts

    async def send(self, payload: Payload, attempt: int = 0) -> ExecutionResult:
        """Sends the properly signed http request with the specified payload"""
        try:
            timestamp = int(time.time() * 1000)

            # we do not want spaces in payload json, since it is crucial for the resulting signature to be valid
            payload_json = json.dumps(payload.__json__()).replace(" ", "")
            signature = self.sign(payload_json, timestamp)

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "x-client-id": self.options.clientId,
                "x-timestamp": str(timestamp),
                "x-signature": signature,
            }

            resp = requests.post(self.options.dsn, data=payload_json, headers=headers)
            data = resp.json() if resp.text else None

            if (
                data
                and isinstance(data, dict)
                and "message" in data
                and data.get("message") == "OK"
            ):
                return success_result(str(data.get("message")))

            return error_result(f"Error executing request: {str(data)}")

        except Exception as ex:
            if attempt < self.max_retry_attempts:
                return io.run(self.retry(payload, attempt + 1))

            return exception_result(ex)

    def sign(self, payload_json: str, timestamp: int) -> str:
        """create an HMAC sha256 signature utilizing the specified payload, timestamp and client id using the client secret"""
        message = f"{self.options.clientId}{timestamp}{payload_json}"
        secret = self.options.clientSecret

        hashed = hmac.new(
            secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
        )

        return hashed.hexdigest()

    async def retry(self, payload: Payload, attempt: int) -> ExecutionResult:
        """Sends an HTTP request asynchronously and returns an ExecutionResult."""
        next_attempt_in = 2**attempt
        return io.run(sc.delay(lambda: self.send(payload, attempt), next_attempt_in))
