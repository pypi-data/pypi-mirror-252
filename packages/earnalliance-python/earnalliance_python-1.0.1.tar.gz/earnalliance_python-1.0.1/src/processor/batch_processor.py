import time
import asyncio as io
from options import NodeOptions
from model.execution_result import ExecutionResult, exception_result, success_result
from transporter.http_transporter import HTTPTransporter
from model.payload import Payload
from model.queue_item import Event, Identifier, QueueItem
from constants import FLUSH_COOLDOWN
from typing import List, Tuple
from utils import Scheduler as sc


class BatchProcessor:
    def __init__(self, transporter: HTTPTransporter, options: NodeOptions):
        self.transporter: HTTPTransporter = transporter
        self.options: NodeOptions = options
        self.queue: List[QueueItem] = []
        self.last_flush = 0
        self.batch_running = False
        self.flush_running = False
        self.event_loop = io.get_event_loop()

    def add_event(self, event: Event) -> io.Future[ExecutionResult]:
        self.queue.append(event)

        if event.event in self.options.flushEvents:
            return io.ensure_future(self.flush())

        return io.ensure_future(self.schedule_batch())

    def add_identifier(self, identifier: Identifier) -> io.Future[ExecutionResult]:
        self.queue.append(identifier)
        return io.ensure_future(self.flush())

    def schedule_batch(self) -> io.Future[ExecutionResult]:
        if len(self.queue) >= self.options.batchSize:
            return io.ensure_future(self.process())

        if not self.batch_running:
            self.batch_running = True
            return io.ensure_future(
                sc.delay(lambda: self.process(), self.options.interval / 1000)
            )

        # batch is currently running
        return io.get_event_loop().run_in_executor(
            None, lambda: success_result("Batch is running")
        )

    async def flush(self) -> ExecutionResult:
        if self.flush_running:
            return success_result("Flush is running")

        self.flush_running = True

        now = time.time() * 1000
        time_since_last_flush = now - self.last_flush

        if time_since_last_flush >= FLUSH_COOLDOWN:
            self.last_flush = now
            return await self.process()

        delay = int(time.time() + (FLUSH_COOLDOWN - time_since_last_flush) / 1000)
        return io.run(sc.delay(lambda: self.process(), delay))

    @staticmethod
    def partition_queue(batch: List[QueueItem]) -> Tuple[List[Event], List[Identifier]]:
        events: List[Event] = []
        identifiers: List[Identifier] = []
        for elem in batch:
            if isinstance(elem, Event):
                events.append(elem)
            elif isinstance(elem, Identifier):
                identifiers.append(elem)

        return events, identifiers

    async def process(self) -> ExecutionResult:
        self.reset_processing()

        batch = self.queue[: self.options.batchSize]
        if not batch:
            return success_result("batch is already procesed")

        self.queue = self.queue[self.options.batchSize :]

        events, identifiers = BatchProcessor.partition_queue(batch)
        payload = Payload(
            gameId=self.options.gameId,
            events=events,
            identifiers=identifiers,
        )

        try:
            return await self.transporter.send(payload)
        except Exception as ex:
            return exception_result(ex)

    def reset_processing(self) -> None:
        if self.batch_running:
            self.batch_running = False

        if self.flush_running:
            self.flush_running = False
