import logging
import voluptuous as vol
from typing import Any, Optional, Tuple

from .idealled import IDEALLEDInstance
from .const import DOMAIN

from homeassistant.const import CONF_MAC
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.components.light import (
    PLATFORM_SCHEMA,
    ATTR_BRIGHTNESS,
    ATTR_HS_COLOR,
    ATTR_EFFECT,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.util.color import match_max_scale
from homeassistant.helpers import device_registry

LOGGER = logging.getLogger(__name__)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({vol.Required(CONF_MAC): cv.string})

async def async_setup_entry(hass, config_entry, async_add_devices):
    instance = hass.data[DOMAIN][config_entry.entry_id]
    await instance.update()
    async_add_devices(
        [IDEALLEDLight(instance, config_entry.data["name"], config_entry.entry_id)]
    )
    #config_entry.async_on_unload(await instance.stop())


class IDEALLEDLight(LightEntity):
    def __init__(
        self, idealledinstance: IDEALLEDInstance, name: str, entry_id: str
    ) -> None:
        self._instance = idealledinstance
        self._entry_id = entry_id
        self._attr_supported_color_modes = {ColorMode.HS, ColorMode.UNKNOWN}
        self._attr_supported_features = LightEntityFeature.EFFECT
        #self._attr_brightness_step_pct = 10
        self._attr_name = name
        self._attr_unique_id = self._instance.mac
        self._instance.local_callback = self.light_local_callback
        
    @property
    def available(self):
        return self._instance.is_on != None

    @property
    def brightness(self):
        return self._instance.brightness

    @property
    def brightness_pct(self):
        return (self._instance.brightness / 255) * 100
    
    @property
    def brightness_step_pct(self):
        return self._attr_brightness_step_pct
    
    @property
    def is_on(self) -> Optional[bool]:
        return self._instance.is_on

    @property
    def effect_list(self):
        return self._instance.effect_list

    @property
    def effect(self):
        return self._instance._effect

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return self._attr_supported_features

    @property
    def supported_color_modes(self) -> int:
        """Flag supported color modes."""
        return self._attr_supported_color_modes

    # @property
    # def rgb_color(self):
    #     """Return the hs color value."""
    #     return self._instance.rgb_color
    
    @property
    def hs_color(self):
        """Return the hs color value."""
        return self._instance.hs_color
    
    @property
    def color_mode(self):
        """Return the color mode of the light."""
        return self._instance._color_mode

    @property
    def device_info(self):
        """Return device info."""
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._instance.mac)
            },
            name=self.name,
            connections={(device_registry.CONNECTION_NETWORK_MAC, self._instance.mac)},
        )

    @property
    def should_poll(self):
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        LOGGER.info("Turn on called.  kwargs: "+str(kwargs))
        if not self.is_on:
            await self._instance.turn_on()
                
        if ATTR_BRIGHTNESS in kwargs and len(kwargs) == 1:
            # Only brightness changed
            LOGGER.debug(f"Only setting brightness: {kwargs[ATTR_BRIGHTNESS]}")
            await self._instance.set_brightness(kwargs[ATTR_BRIGHTNESS])
               
        # if ATTR_RGB_COLOR in kwargs:
        #     if kwargs[ATTR_RGB_COLOR] != self.rgb_color:
        #         self._effect = None
        #         bri = kwargs[ATTR_BRIGHTNESS] if ATTR_BRIGHTNESS in kwargs else self._instance._brightness_pct
        #         await self._instance.set_rgb_color(kwargs[ATTR_RGB_COLOR], bri)
        
        if ATTR_HS_COLOR in kwargs:
            if kwargs[ATTR_HS_COLOR] != self.hs_color:
                self._effect = None
                bri = kwargs[ATTR_BRIGHTNESS] if ATTR_BRIGHTNESS in kwargs else self._instance._brightness
                LOGGER.debug(f"Setting color: {kwargs[ATTR_HS_COLOR]}. Brightness: {bri}")
                await self._instance.set_rgb_color(kwargs[ATTR_HS_COLOR], bri)

        if ATTR_EFFECT in kwargs:
            if kwargs[ATTR_EFFECT] != self.effect:
                self._effect = kwargs[ATTR_EFFECT]
                bri = kwargs[ATTR_BRIGHTNESS] if ATTR_BRIGHTNESS in kwargs else self._instance._brightness
                await self._instance.set_effect(kwargs[ATTR_EFFECT], bri)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._instance.turn_off()
        self.async_write_ha_state()

    async def async_update(self) -> None:
        LOGGER.debug("async update called")
        await self._instance.update()
        self.async_write_ha_state()
    
    def light_local_callback(self):
        self.async_write_ha_state()

    async def update_ha_state(self) -> None:
        await self._instance.update()
        self.async_write_ha_state()
