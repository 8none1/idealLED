import asyncio
from .idealled import IDEALLEDInstance
from typing import Any

from bluetooth_data_tools import human_readable_name
from homeassistant import config_entries
from homeassistant.const import CONF_MAC
import voluptuous as vol
from homeassistant.helpers.device_registry import format_mac
from homeassistant.data_entry_flow import FlowResult
from homeassistant.core import callback
from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo

from .const import DOMAIN, CONF_RESET, CONF_DELAY
import logging

LOGGER = logging.getLogger(__name__)
DATA_SCHEMA = vol.Schema({("host"): str})

class DeviceData(BluetoothData):
    def __init__(self, discovery_info) -> None:
        self._discovery = discovery_info
        manu_data = next(iter(self._discovery.manufacturer_data.values()), None)
        # LOGGER.debug(f"Manu data keys: {self._discovery.manufacturer_data.keys()}")
        # LOGGER.debug(f"Manufacturer Data: {manu_data}")
        if discovery_info.name.lower().startswith("isp-"):
            try:
                if manu_data:
                    LOGGER.debug(f"DeviceData: {discovery_info}")
                    LOGGER.debug(f"Name: {discovery_info.name}")
                    LOGGER.debug(f"Manufacturer Data: {manu_data}")
                    LOGGER.debug(f"Manufacturer Data (hex): {[f'0x{byte:02x}' for byte in manu_data]}")
            except:
                raise Exception("Error parsing manufacturer data")
        
        LOGGER.debug("Discovered bluetooth devices, DeviceData, : %s , %s", self._discovery.address, self._discovery.name)

    def supported(self):
        return self._discovery.name.lower().startswith("isp-")

    def address(self):
        return self._discovery.address

    def get_device_name(self):
        return human_readable_name(None, self._discovery.name, self._discovery.address)

    def name(self):
        return human_readable_name(None, self._discovery.name, self._discovery.address)

    def rssi(self):
        return self._discovery.rssi

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        LOGGER.debug("Parsing BLE advertisement data: %s", service_info)
        
class iDealLedFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self) -> None:
        self.mac = None
        self._device = None
        self._instance = None
        self.name = None
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_device: DeviceData | None = None
        self._discovered_devices = []

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        """Handle the bluetooth discovery step."""
        LOGGER.debug("Discovered bluetooth devices, step bluetooth, : %s , %s", discovery_info.address, discovery_info.name)
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        device = DeviceData(discovery_info)
        self.context["title_placeholders"] = {"name": device.name()}
        if device.supported():
            self._discovered_devices.append(device)
            return await self.async_step_bluetooth_confirm()
        else:
            return self.async_abort(reason="not_supported")

    async def async_step_bluetooth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovery."""
        LOGGER.debug("Discovered bluetooth devices, step bluetooth confirm, : %s", user_input)
        self._set_confirm_only()
        return await self.async_step_user()
    
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the user step to pick discovered device."""
        if user_input is not None:
            self.mac = user_input[CONF_MAC]
            if "title_placeholders" in self.context:
                self.name = self.context["title_placeholders"]["name"]
            if 'source' in self.context.keys() and self.context['source'] == "user":
                LOGGER.debug(f"User context.  discovered devices: {self._discovered_devices}")
                for each in self._discovered_devices:
                    LOGGER.debug(f"Address: {each.address()}")
                    if each.address() == self.mac:
                        self.name = each.get_device_name()
            if self.name is None: self.name = self.mac
            await self.async_set_unique_id(self.mac, raise_on_progress=False)
            self._abort_if_unique_id_configured()
            return await self.async_step_validate()            

        current_addresses = self._async_current_ids()
        for discovery_info in async_discovered_service_info(self.hass):
            self.mac = discovery_info.address
            if self.mac in current_addresses:
                LOGGER.debug("Device %s in current_addresses", (self.mac))
                continue
            if (device for device in self._discovered_devices if device.address == self.mac) == ([]):
                LOGGER.debug("Device %s in discovered_devices", (device))
                continue
            device = DeviceData(discovery_info)
            if device.supported():
                self._discovered_devices.append(device)
        
        if not self._discovered_devices:
            return await self.async_step_manual()

        LOGGER.debug("Discovered supported devices: %s - %s", self._discovered_devices[0].name(), self._discovered_devices[0].address())

        mac_dict = { dev.address(): dev.name() for dev in self._discovered_devices }
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(
                {
                    vol.Required(CONF_MAC): vol.In(mac_dict),
                }
            ),
            errors={})

    async def async_step_validate(self, user_input: "dict[str, Any] | None" = None):
        if user_input is not None:
            if "flicker" in user_input:
                if user_input["flicker"]:
                    return self.async_create_entry(title=self.name, data={CONF_MAC: self.mac, "name": self.name})
                return self.async_abort(reason="cannot_validate")
            
            if "retry" in user_input and not user_input["retry"]:
                return self.async_abort(reason="cannot_connect")

        error = await self.toggle_light()

        if error:
            return self.async_show_form(
                step_id="validate", data_schema=vol.Schema(
                    {
                        vol.Required("retry"): bool
                    }
                ), errors={"base": "connect"})
        
        return self.async_show_form(
            step_id="validate", data_schema=vol.Schema(
                {
                    vol.Required("flicker"): bool
                }
            ), errors={})

    async def async_step_manual(self, user_input: "dict[str, Any] | None" = None):
        if user_input is not None:            
            self.mac = user_input[CONF_MAC]
            self.name = user_input["name"]
            await self.async_set_unique_id(format_mac(self.mac))
            return await self.async_step_validate()

        return self.async_show_form(
            step_id="manual", data_schema=vol.Schema(
                {
                    vol.Required(CONF_MAC): str,
                    vol.Required("name"): str
                }
            ), errors={})

    async def toggle_light(self):
        if not self._instance:
            self._instance = IDEALLEDInstance(self.mac, False, 120, self.hass)
        try:
            await self._instance.update()
            await self._instance.turn_on()
            await asyncio.sleep(1)
            await self._instance.turn_off()
            await asyncio.sleep(1)
            await self._instance.turn_on()
            await asyncio.sleep(1)
            await self._instance.turn_off()
        except (Exception) as error:
            return error
        finally:
            await self._instance.stop()

    @staticmethod
    @callback
    def async_get_options_flow(entry: config_entries.ConfigEntry):
        return OptionsFlowHandler(entry)

class OptionsFlowHandler(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, _user_input=None):
        """Manage the options."""
        return await self.async_step_user()
    
    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}
        options = self.config_entry.options or {CONF_RESET: False,CONF_DELAY: 120}
        if user_input is not None:
            return self.async_create_entry(title="", data={CONF_RESET: user_input[CONF_RESET], CONF_DELAY: user_input[CONF_DELAY]})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_DELAY, default=options.get(CONF_DELAY)): int
                }
            ), errors=errors
        )
