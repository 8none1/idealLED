"""Number platform for ideal_led integration."""
import logging
from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import device_registry

from .const import DOMAIN
from .idealled import IDEALLEDInstance

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    instance = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [IDEALLEDSpeedSlider(instance, "Effect Speed", config_entry.entry_id)]
    )


class IDEALLEDSpeedSlider(NumberEntity):
    """Representation of an IDEAL LED effect speed slider."""

    def __init__(
        self, instance: IDEALLEDInstance, name: str, entry_id: str
    ) -> None:
        """Initialize the speed slider."""
        self._instance = instance
        self._entry_id = entry_id
        self._attr_name = f"{instance.name} {name}"
        self._attr_unique_id = f"{instance.mac}_effect_speed"
        self._attr_native_min_value = 1
        self._attr_native_max_value = 100
        self._attr_native_step = 1
        self._attr_mode = NumberMode.SLIDER
        self._attr_icon = "mdi:speedometer"

        # Register callback for updates from the device
        self._instance.speed_local_callback = self.speed_local_callback

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, self._instance.mac)
            },
            name=self._instance.name,
            connections={(device_registry.CONNECTION_NETWORK_MAC, self._instance.mac)},
            model=self._instance._model,
            sw_version=self._instance.firmware_version
        )

    @property
    def native_value(self) -> float:
        """Return the current effect speed."""
        return self._instance._effect_speed

    async def async_set_native_value(self, value: float) -> None:
        """Set the effect speed."""
        LOGGER.debug(f"Setting effect speed to {int(value)}")
        await self._instance.set_effect_speed(int(value))
        self.async_write_ha_state()

    @callback
    def speed_local_callback(self) -> None:
        """Handle updates from the device."""
        self.async_write_ha_state()
