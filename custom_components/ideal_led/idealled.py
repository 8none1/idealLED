import asyncio
#from datetime import datetime
from homeassistant.components import bluetooth
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.components.light import (ColorMode)
from Crypto.Cipher import AES
from bleak.backends.device import BLEDevice
from bleak.backends.service import BleakGATTCharacteristic, BleakGATTServiceCollection
from bleak.exc import BleakDBusError
from bleak_retry_connector import BLEAK_RETRY_EXCEPTIONS as BLEAK_EXCEPTIONS
from bleak_retry_connector import (
    BleakClientWithServiceCache,
    BleakError,
    BleakNotFoundError,
    ble_device_has_changed,
    establish_connection,
)
from typing import Any, TypeVar, cast, Tuple
from collections.abc import Callable
import traceback
import logging
import colorsys

# Add effects information in a separate file because there is a LOT of boilerplate.

LOGGER = logging.getLogger(__name__)

EFFECT_01 = "Effect 01"
EFFECT_02 = "Effect 02"
EFFECT_03 = "Effect 03"
EFFECT_04 = "Effect 04"
EFFECT_05 = "Effect 05"
EFFECT_06 = "Effect 06"
EFFECT_07 = "Effect 07"
EFFECT_08 = "Effect 08"
EFFECT_09 = "Effect 09"
EFFECT_10 = "Effect 10"

EFFECT_MAP = {
    EFFECT_01: 1,
    EFFECT_02: 2,
    EFFECT_03: 3,
    EFFECT_04: 4,
    EFFECT_05: 5,
    EFFECT_06: 6,
    EFFECT_07: 7,
    EFFECT_08: 8,
    EFFECT_09: 9,
    EFFECT_10: 10,
}

EFFECT_LIST = sorted(EFFECT_MAP)
EFFECT_ID_NAME = {v: k for k, v in EFFECT_MAP.items()}

NAME_ARRAY = ["ISP-"]
WRITE_CMD_CHARACTERISTIC_UUIDS = ["d44bc439-abfd-45a2-b575-925416129600"]
WRITE_COL_CHARACTERISTIC_UUIDS = ["d44bc439-abfd-45a2-b575-92541612960a"]
NOTIFY_CHARACTERISTIC_UUIDS    = ["d44bc439-abfd-45a2-b575-925416129601"]
SECRET_ENCRYPTION_KEY = bytes([0x34, 0x52, 0x2A, 0x5B, 0x7A, 0x6E, 0x49, 0x2C, 0x08, 0x09, 0x0A, 0x9D, 0x8D, 0x2A, 0x23, 0xF8])


DEFAULT_ATTEMPTS = 3
BLEAK_BACKOFF_TIME = 0.25
RETRY_BACKOFF_EXCEPTIONS = (BleakDBusError)

WrapFuncType = TypeVar("WrapFuncType", bound=Callable[..., Any])

def bytearray_to_hex_format(byte_array):
    hex_strings = ["0x{:02x}".format(byte) for byte in byte_array]
    return hex_strings

def retry_bluetooth_connection_error(func: WrapFuncType) -> WrapFuncType:
    async def _async_wrap_retry_bluetooth_connection_error(
        self: "IDEALLEDInstance", *args: Any, **kwargs: Any
    ) -> Any:
        attempts = DEFAULT_ATTEMPTS
        max_attempts = attempts - 1

        for attempt in range(attempts):
            try:
                return await func(self, *args, **kwargs)
            except BleakNotFoundError:
                # The lock cannot be found so there is no
                # point in retrying.
                raise
            except RETRY_BACKOFF_EXCEPTIONS as err:
                if attempt >= max_attempts:
                    LOGGER.debug(
                        "%s: %s error calling %s, reach max attempts (%s/%s)",
                        self.name,
                        type(err),
                        func,
                        attempt,
                        max_attempts,
                        exc_info=True,
                    )
                    raise
                LOGGER.debug(
                    "%s: %s error calling %s, backing off %ss, retrying (%s/%s)...",
                    self.name,
                    type(err),
                    func,
                    BLEAK_BACKOFF_TIME,
                    attempt,
                    max_attempts,
                    exc_info=True,
                )
                await asyncio.sleep(BLEAK_BACKOFF_TIME)
            except BLEAK_EXCEPTIONS as err:
                if attempt >= max_attempts:
                    LOGGER.debug(
                        "%s: %s error calling %s, reach max attempts (%s/%s): %s",
                        self.name,
                        type(err),
                        func,
                        attempt,
                        max_attempts,
                        err,
                        exc_info=True,
                    )
                    raise
                LOGGER.debug(
                    "%s: %s error calling %s, retrying  (%s/%s)...: %s",
                    self.name,
                    type(err),
                    func,
                    attempt,
                    max_attempts,
                    err,
                    exc_info=True,
                )

    return cast(WrapFuncType, _async_wrap_retry_bluetooth_connection_error)

class IDEALLEDInstance:
    def __init__(self, address, reset: bool, delay: int, hass) -> None:
        self.loop = asyncio.get_running_loop()
        self._mac = address
        self._reset = reset
        self._delay = delay
        self._hass = hass
        self._device: BLEDevice | None = None
        self._device = bluetooth.async_ble_device_from_address(self._hass, address)
        if not self._device:
            raise ConfigEntryNotReady(
                f"You need to add bluetooth integration (https://www.home-assistant.io/integrations/bluetooth) or couldn't find a nearby device with address: {address}"
            )
        self._connect_lock: asyncio.Lock = asyncio.Lock()
        self._client: BleakClientWithServiceCache | None = None
        self._disconnect_timer: asyncio.TimerHandle | None = None
        self._cached_services: BleakGATTServiceCollection | None = None
        self._expected_disconnect = False
        self._is_on = None
        #self._rgb_color = (255,0,0)
        self._hs_color = (0,0)
        self._brightness = 255
        self._effect = None
        self._effect_speed = 0x64
        self._color_mode = ColorMode.HS
        self._write_uuid = None
        self._write_colour_uuid = None
        self._read_uuid = None
        self._turn_on_cmd = None
        self._turn_off_cmd = None
        self._model = self._detect_model()
        self._on_update_callbacks = []
        
        LOGGER.debug(
            "Model information for device %s : ModelNo %s. MAC: %s",
            self._device.name,
            self._model,
            self._mac,
        )

    def _detect_model(self):
        x = 0
        for name in NAME_ARRAY:
            if self._device.name.lower().startswith(name.lower()): # TODO: match on BLE provided model instead of name
                return x
            x = x + 1

    async def _write(self, data: bytearray):
        """Send command to device and read response."""
        await self._ensure_connected()
        cipher = AES.new(SECRET_ENCRYPTION_KEY, AES.MODE_ECB)
        ciphered_data = cipher.encrypt(data)
        await self._write_while_connected(ciphered_data)

    async def _write_colour_data(self, data: bytearray):
        """Send command to device and read response."""
        await self._ensure_connected()
        await self._write_colour_while_connected(data)

    async def _write_while_connected(self, data: bytearray):
        LOGGER.debug(f"Writing data to {self.name}: {data}")
        await self._client.write_gatt_char(self._write_uuid, data, False)
    
    async def _write_colour_while_connected(self, data: bytearray):
        LOGGER.debug(f"Writing colour data to {self.name}: {data}")
        await self._client.write_gatt_char(self._write_colour_uuid, data, False)
    
    def _notification_handler(self, _sender: BleakGATTCharacteristic, data: bytearray) -> None:
        # This doesn't work.  I can't get the controller to send notifications.
        """Handle BLE notifications from the device.  Update internal state to reflect the device state."""
        cipher = AES.new(SECRET_ENCRYPTION_KEY, AES.MODE_ECB)
        clear_data = cipher.decrypt(data)
        LOGGER.debug(f"BLE Notification: {self.name}: {bytearray_to_hex_format(clear_data)}")
        #self.local_callback()


    @property
    def mac(self):
        return self._device.address

    @property
    def reset(self):
        return self._reset

    @property
    def name(self):
        return self._device.name

    @property
    def rssi(self):
        return self._device.rssi

    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness 
    
    # @property
    # def brightness_pct(self):
    #     return int(self._brightness / 255 * 100)

    @property
    def hs_color(self):
        return self._hs_color

    @property
    def effect_list(self) -> list[str]:
        return EFFECT_LIST

    @property
    def effect(self):
        return self._effect
    
    @property
    def color_mode(self):
        return self._color_mode

    async def set_brightness(self, brightness: int):
        LOGGER.debug("Brightness only requested: "+str(brightness))
        LOGGER.debug("Current brightness: "+str(self._brightness))
        if brightness == self._brightness:
          return
        else:
          brightness = max(0, min(255, brightness))
          self._brightness = brightness
          if self._effect is not None:
            await self.set_effect(self._effect, brightness)
          else:
            await self.set_rgb_color(self._hs_color, brightness)
          
    @retry_bluetooth_connection_error
    async def set_rgb_color(self, hs_col: Tuple[int, int], brightness: int | None = None):
        LOGGER.debug(f"X Current brightness: {self._brightness}")
        if None in hs_col and self._hs_color is not None:
          hs_col = self._hs_color
        else:
            self._hs_color = hs_col
        
        LOGGER.debug("HS colour requested: %s", hs_col)
        rgb_color = colorsys.hsv_to_rgb(hs_col[0] / 360, hs_col[1] / 100, 1)
        rgb_color = [round(x * 255) for x in rgb_color]
        LOGGER.debug("Calculated RGB colour: %s", rgb_color)
        self._effect = None
        self._color_mode = ColorMode.HS
        if brightness is None:
            LOGGER.debug("Brightness not specified, using current value: %s", self._brightness)
            if self._brightness is None:
                self._brightness = 255
            else:
                brightness = self._brightness
        else:
            self._brightness = brightness
        brightness_percent = int(brightness * 100 / 255)
        # Now adjust the RBG values to match the brightness
        red =   int(rgb_color[0] * brightness / 255)
        green = int(rgb_color[1] * brightness / 255)
        blue =  int(rgb_color[2] * brightness / 255)
        LOGGER.debug("RGB colour adjusted for brightness: %s", (red, green, blue))
        # RGB packet
        rgb_packet = bytearray.fromhex("0F 53 47 4C 53 00 00 64 50 1F 00 00 1F 00 00 32")
        red   = int(red >> 3) # You CAN send 8 bit colours to this thing, but you probably shouldn't for power reasons.  Thanks to the good folks at Hacker News for that insight.
        green = int(green >> 3)
        blue  = int(blue >> 3)
        rgb_packet[9] = red
        rgb_packet[12] = red
        rgb_packet[10] = green
        rgb_packet[13] = green
        rgb_packet[11] = blue
        rgb_packet[14] = blue
        await self._write(rgb_packet)


    @retry_bluetooth_connection_error
    # effect, reverse=0, speed=50, saturation=50, colour_data=COLOUR_DATA
    async def set_effect(self, effect: str, brightness: int | None = NotImplemented):
        if effect not in EFFECT_LIST:
            LOGGER.error("Effect %s not supported", effect)
            return
        self._effect = effect
        self._color_mode = None
        effect_id = EFFECT_MAP.get(effect)
        if effect_id > 11: effect = 11
        brightness_pct = int(brightness /255 * 100)
        packet = bytearray.fromhex("0A 4D 55 4C 54 08 00 64 50 07 32 00 00 00 00 00")
        packet[5]  = effect_id
        packet[6]  = 0 # reverse
        packet[8]  = 50 # speed
        packet[10] = brightness_pct # 2024-11-16 Was: 100 # This was here before: brightness_pct # 50 # saturation (brightness?)
        await self._write(packet)
        await self.write_colour_data()
    
    @retry_bluetooth_connection_error
    async def write_colour_data(self):
        # This is sent after switching to an effect to tell the device what sort of pattern to show.
        # In the app you can edit this yourself, but HA doesn't have the UI for such a thing
        # so for now I'm just going to hardcode it to a rainbow pattern.  You could change this to
        # whatever you want, but for an effect the maximum length is 7 colours.
        brightness_pct = (self._brightness / 255) * 100
        colour_list = []
        colour_divisions = int(360 / 7)
        for i in range(7):
            h = i * colour_divisions
            r, g, b = colorsys.hsv_to_rgb(h / 360, 1, brightness_pct / 100.0)
            r = int(r * 255)
            g = int(g * 255)
            b = int(b * 255)
            colour_list.append((r, g, b))
        #print(f"Colour list: {colour_list}")
        length = len(colour_list)
        colour_data = []
        colour_data.append(length*3) # 3 bytes per colour
        colour_data.append(0) # Don't know what this is, perhaps just a separator
        for colour in colour_list:
            colour_data.append(colour[0])
            colour_data.append(colour[1])
            colour_data.append(colour[2])
        await self._write_colour_data(colour_data)


    @retry_bluetooth_connection_error
    async def turn_on(self):
        packet = bytearray.fromhex("05 54 55 52 4E 01 00 00 00 00 00 00 00 00 00 00")
        packet[5] = 1
        await self._write(packet)
        self._is_on = True

    @retry_bluetooth_connection_error
    async def turn_off(self):
        packet = bytearray.fromhex("05 54 55 52 4E 01 00 00 00 00 00 00 00 00 00 00")
        packet[5] = 0
        await self._write(packet)
        self._is_on = False

    @retry_bluetooth_connection_error
    async def update(self):
        LOGGER.debug("%s: Update in lwdnetwf called", self.name)
        try:
            await self._ensure_connected()
            self._is_on = False
        except Exception as error:
            self._is_on = None # failed to connect, this should mark it as unavailable
            LOGGER.error("Error getting status: %s", error)
            track = traceback.format_exc()
            LOGGER.debug(track)

    async def _ensure_connected(self) -> None:
        """Ensure connection to device is established."""
        if self._connect_lock.locked():
            LOGGER.debug(
                "%s: Connection already in progress, waiting for it to complete",
                self.name,
            )
        if self._client and self._client.is_connected:
            self._reset_disconnect_timer()
            return
        async with self._connect_lock:
            # Check again while holding the lock
            if self._client and self._client.is_connected:
                self._reset_disconnect_timer()
                return
            LOGGER.debug("%s: Connecting", self.name)
            client = await establish_connection(
                BleakClientWithServiceCache,
                self._device,
                self.name,
                self._disconnected,
                cached_services=self._cached_services,
                ble_device_callback=lambda: self._device,
            )
            LOGGER.debug("%s: Connected", self.name)
            resolved = self._resolve_characteristics(client.services)
            if not resolved:
                # Try to handle services failing to load
                resolved = self._resolve_characteristics(await client.get_services())
            self._cached_services = client.services if resolved else None

            self._client = client
            self._reset_disconnect_timer()

            # Subscribe to notification is needed for LEDnetWF devices to accept commands
            self._notification_callback = self._notification_handler
            await client.start_notify(self._read_uuid, self._notification_callback)
            LOGGER.debug("%s: Subscribed to notifications", self.name)


    def _resolve_characteristics(self, services: BleakGATTServiceCollection) -> bool:
        """Resolve characteristics."""
        for characteristic in NOTIFY_CHARACTERISTIC_UUIDS:
            if char := services.get_characteristic(characteristic):
                self._read_uuid = char
                LOGGER.debug("%s: Read UUID: %s", self.name, self._read_uuid)
                break
        for characteristic in WRITE_CMD_CHARACTERISTIC_UUIDS:
            if char := services.get_characteristic(characteristic):
                self._write_uuid = char
                LOGGER.debug("%s: Write UUID: %s", self.name, self._write_uuid)
                break
        for characteristic in WRITE_COL_CHARACTERISTIC_UUIDS:
            if char := services.get_characteristic(characteristic):
                self._write_colour_uuid = char
                LOGGER.debug("%s: Write colour UUID: %s", self.name, self._write_colour_uuid)
                break
        return bool(self._read_uuid and self._write_uuid and self._write_colour_uuid)

    def _reset_disconnect_timer(self) -> None:
        """Reset disconnect timer."""
        if self._disconnect_timer:
            self._disconnect_timer.cancel()
        self._expected_disconnect = False
        if self._delay is not None and self._delay != 0:
            LOGGER.debug(
                "%s: Configured disconnect from device in %s seconds",
                self.name,
                self._delay
            )
            self._disconnect_timer = self.loop.call_later(self._delay, self._disconnect)

    def _disconnected(self, client: BleakClientWithServiceCache) -> None:
        """Disconnected callback."""
        if self._expected_disconnect:
            LOGGER.debug("%s: Disconnected from device", self.name)
            return
        LOGGER.warning("%s: Device unexpectedly disconnected", self.name)

    def _disconnect(self) -> None:
        """Disconnect from device."""
        self._disconnect_timer = None
        asyncio.create_task(self._execute_timed_disconnect())

    async def stop(self) -> None:
        """Stop the LEDBLE."""
        LOGGER.debug("%s: Stop", self.name)
        await self._execute_disconnect()

    async def _execute_timed_disconnect(self) -> None:
        """Execute timed disconnection."""
        LOGGER.debug(
            "%s: Disconnecting after timeout of %s",
            self.name,
            self._delay
        )
        await self._execute_disconnect()

    async def _execute_disconnect(self) -> None:
        """Execute disconnection."""
        async with self._connect_lock:
            read_char = self._read_uuid
            client = self._client
            self._expected_disconnect = True
            self._client = None
            self._write_uuid = None
            self._read_uuid = None
            if client and client.is_connected:
                await client.stop_notify(read_char) #  TODO:  I don't think this is needed.  Bleak docs say it isnt.
                await client.disconnect()
            LOGGER.debug("%s: Disconnected", self.name)
    
    def local_callback(self):
        # Placeholder to be replaced by a call from light.py
        # I can't work out how to plumb a callback from here to light.py
        return

