#!/usr/bin/env python

import asyncio
import signal
from typing import Callable, Optional
from concord4ws.types import (
    ArmLevel,
    ArmMode,
    ArmOptions,
    ArmingLevelData,
    CommandSendableMessage,
    ConcordArmCommand,
    ConcordDisarmCommand,
    ConcordToggleChimeCommand,
    DisarmOptions,
    Keypress,
    PanelData,
    PartitionData,
    ReceivableMessage,
    SendableMessage,
    State,
    ZoneData,
    ZoneStatusData,
    arming_level_to_partition_arming_level,
)
from pydantic import TypeAdapter
import websockets
import logging

logger = logging.getLogger("concord4ws")


class Concord4WSClient:
    _connected: bool = False
    _connect_attempt: int = 0
    _callbacks = dict[str, set[Callable[[], None]]]()
    _initialized: bool = False
    _state: State
    _ws: websockets.WebSocketClientProtocol

    def __init__(self, host: str, port: str | int):
        self.host = host
        self.port = port
        self._loop = asyncio.get_event_loop()

    @property
    def state(self):
        return self._state

    @property
    def connected(self):
        return self._connected

    async def test_connect(self) -> bool:
        try:
            async with websockets.connect(f"ws://{self.host}:{self.port}"):
                return True
        except Exception as _:
            return False

    async def _handle_signal_exit(self):
        logger.info("received signal, closing connection")
        if self._ws is not None and not self._ws.closed:
            await self._ws.close()

        self._connected = False

        self._loop.stop()
        self._loop.close()

    async def _event_loop(self):
        self._loop.add_signal_handler(
            signal.SIGTERM, lambda: asyncio.create_task(self._handle_signal_exit())
        )

        async for ws in websockets.connect(f"ws://{self.host}:{self.port}"):
            try:
                self._connected = True
                self._connect_attempt = 0
                self._ws = ws

                while True:
                    async for message in ws:
                        logger.debug("message received: %s", message)
                        self._handle_message(message)

            except websockets.ConnectionClosed:
                self._connected = False
                self._connect_attempt += 1

                continue

    def _handle_message(self, message: websockets.Data) -> None:
        """Handle incoming message from server."""
        try:
            recv: ReceivableMessage = TypeAdapter(ReceivableMessage).validate_json(
                message
            )
            logger.debug("decoded message as: %s", recv)

            if recv.type == "state":
                logger.debug("updating state")
                self._state = recv.data
                self._initialized = True

            if recv.type == "message":
                match recv.data.type:
                    case "panelType":
                        logger.debug("handling panel type")
                        self._handle_panel_type(recv.data.data)
                    case "zoneData":
                        logger.debug("handling zone data")
                        self._handle_zone_data(recv.data.data)
                    case "zoneStatus":
                        logger.debug("handling zone status data")
                        self._handle_zone_status_data(recv.data.data)
                    case "partitionData":
                        logger.debug("handling partition data")
                        self._handle_partition_data(recv.data.data)
                    case "armingLevel":
                        logger.debug("handling arming level data")
                        self._handle_arming_level_data(recv.data.data)
                    case _:
                        logger.debug("unhandled message type")

        except Exception as e:
            logger.error(e)

    def _handle_panel_type(self, data: PanelData) -> None:
        """Handle panel type message."""
        self._state.panel = data

    def _handle_zone_data(self, data: ZoneData) -> None:
        """Handle zone data message."""
        self._state.zones[data.id()] = data

        if data.callback_id() in self._callbacks:
            for callback in self._callbacks[data.id()]:
                callback()

    def _handle_zone_status_data(self, data: ZoneStatusData) -> None:
        """Handle zone status data message."""
        self._state.zones[data.zone_id()].zone_status = data.zone_status

        if data.callback_id() in self._callbacks:
            for callback in self._callbacks[data.callback_id()]:
                callback()

    def _handle_partition_data(self, data: PartitionData) -> None:
        """Handle partition data message."""
        self._state.partitions[data.id()] = data

        if data.callback_id() in self._callbacks:
            for callback in self._callbacks[data.callback_id()]:
                callback()

    def _handle_arming_level_data(self, data: ArmingLevelData) -> None:
        """Handle arming level data message."""
        self._state.partitions[
            data.partition_number
        ].arming_level = arming_level_to_partition_arming_level(data.arming_level)

        if data.callback_id() in self._callbacks:
            for callback in self._callbacks[data.callback_id()]:
                callback()

    def register_callback(
        self, zone_or_part_id: str, callback: Callable[[], None]
    ) -> None:
        """Register callback, called when zone or partition specified changes state."""
        logger.debug("registering callback for: %s", zone_or_part_id)
        self._callbacks.setdefault(zone_or_part_id, set()).add(callback)

    def remove_callback(
        self, zone_or_part_id: str, callback: Callable[[], None]
    ) -> None:
        """Remove previously registered callback."""
        logger.debug("removing callback for: %s", zone_or_part_id)
        self._callbacks[zone_or_part_id].remove(callback)

    async def connect(self) -> None:
        """Connect to Concord4WS."""
        logger.info("connecting to concord4ws server")

        self._loop.create_task(self._event_loop())

        # wait for first message from server to initialize state
        while not self._initialized:
            await asyncio.sleep(0.1)

        logger.info("connected to concord4ws server")

    async def disconnect(self) -> None:
        """Disconnect from Concord4WS."""
        if not self._connected:
            logger.error("cannot disconnect, not connected")
            return

        logger.info("disconnecting from concord4ws server")

        self._loop.stop()
        self._loop.close()
        self._loop = asyncio.get_event_loop()

        self._connected = False

    async def send(self, message: SendableMessage) -> None:
        """Send message to server."""
        if not self._connected:
            logger.error("cannot send message, not connected")
            raise Concord4WSClientError("not connected to server")

        logger.debug("sending message: %s", message)

        await self._ws.send(message.model_dump_json())

    async def arm(
        self,
        mode: ArmMode,
        code: list[Keypress],
        level: Optional[ArmLevel] = None,
        partition: Optional[int] = None,
    ) -> None:
        """Arm partition."""

        await self.send(
            CommandSendableMessage(
                data=ConcordArmCommand(
                    params=ArmOptions(
                        mode=mode, code=code, level=level, partition=partition
                    )
                )
            )
        )

    async def disarm(
        self,
        code: list[Keypress],
        partition: Optional[int] = None,
    ) -> None:
        """Disarm partition."""

        await self.send(
            CommandSendableMessage(
                data=ConcordDisarmCommand(
                    params=DisarmOptions(code=code, partition=partition)
                )
            )
        )

    async def toggle_chime(self, partition: Optional[int]) -> None:
        """Toggle chime for partition."""

        await self.send(
            CommandSendableMessage(data=ConcordToggleChimeCommand(params=partition))
        )


class Concord4WSClientError(Exception):
    """Class for exceptions in Concord4WSClient."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
