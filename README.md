# iDeal LED control

![image](https://github.com/8none1/idealLED/assets/6552931/c5fcd8fc-440a-48dd-abe4-d6fdd2e4a422)

## Supported Models

Devices are coming on to the market which report as IDL or ISP lights but which use a different protocol.  Support for these lights can be added by a sample of the lights will be needed OR the gathering of `btsnoop` debug logs from an Android device.  If you are willing to help gather the data and test the new code, please log an issue.

## Supported Features

- On / Off
- Set RGB colour of entire strip
- Set DIY LED patterns (not supported in Home Assistant)
- Set brightness
- Set effect & effect speed
- Bulk paint entire strip using collections feature
- Automatic discovery of supported devices in Home Assistant

## Not supported

- Discovery of current light state
- On-chip timer functionality

## Home Assistant

There is a Home Assistant custom component to let you control these lights.

### Installation

Add this repo to HACS as a custom repo. Click through:

- HACS -> Integrations -> Top right menu -> Custom Repositories
- Paste the Github URL to this repo in to the Repository box
- Choose category Integration
- Click Add
- The repo should show up in HACS as a new integration.  Click on it and choose `DOWNLOAD`.
- Restart Home Assistant
- iDeal LED devices should start to appear in your Integrations page

## Other tools

There are a few other tools in this repo that might help you improve support or test your own lights.

- The btsnoop directory has a few HCI log dumps if you want to look at the raw values
- `aes_decrypt.py` was used to test the encryption implementation
- `att_protocol.md` has notes on the protocol and the Android companion app

## An important note on upgrades

As bugs are fixed and new features are added it might be necessary to delete your existing devices and re-add them.  If you experience strange behaviour after an upgrade please try to delete the device and re-add it.  If this doesn't help, open an issue describing the problem.

## Warning

I have bricked one set of lights by sending invalid data to them while building this integration.  Use this repo at your own risk.
You should be careful when sending bytes to these lights which are outside of the already discovered values.

You can read more on this here: https://www.whizzy.org/2023-12-14-bricked-xmas/

As far as I can tell this integration does not use any unsafe values by default.  If you know otherwise, please open an issue, ideally with an accompanying PR.

## Enabling Debug Logging

If you're experiencing issues with the integration or want to help troubleshoot problems, you can enable debug logging for this integration in Home Assistant.

### Method 1: Using configuration.yaml (Persistent)

Add the following to your `configuration.yaml` file:

```yaml
logger:
  default: info
  logs:
    custom_components.ideal_led: debug
```

After adding this configuration, restart Home Assistant for the changes to take effect.

### Method 2: Using the Home Assistant UI (Temporary)

For temporary debugging without restarting Home Assistant:

1. Go to **Settings** → **Devices & Services**
2. Find the **iDeal LED** integration
3. Click the three-dot menu (⋮) on the integration card
4. Select **Enable debug logging**

This will immediately start capturing debug logs. When you're done debugging:

1. Return to the integration
2. Click the three-dot menu (⋮) again
3. Select **Disable debug logging**

A download will be offered containing the captured debug logs.

### Method 3: Using Developer Tools (Temporary)

1. Go to **Developer Tools** → **Services**
2. Search for and select `logger.set_level`
3. Enter the following in the YAML editor:

```yaml
service: logger.set_level
data:
  custom_components.ideal_led: debug
```

4. Click **Call Service**

This enables debug logging immediately without a restart. The setting will revert to default after Home Assistant restarts.

### Viewing the Logs

You can view the logs in several ways:

#### Via Home Assistant UI

1. Go to **Settings** → **System** → **Logs**
2. Click **Load Full Logs** to see all entries
3. Use the search/filter to look for `ideal_led` entries

#### Via Command Line (Docker)

```bash
docker logs -f homeassistant 2>&1 | grep ideal_led
```

#### Via Command Line (Home Assistant OS / Supervised)

```bash
ha core logs --follow | grep ideal_led
```

#### Via Command Line (Core Installation)

Check your Home Assistant log file location (typically `home-assistant.log` in your config directory):

```bash
tail -f /path/to/config/home-assistant.log | grep ideal_led
```

### What to Include in Bug Reports

When opening an issue, please include:

1. **Debug logs** - Enable debug logging, reproduce the issue, then capture the relevant log entries
2. **Device information** - The model/type of your LED device (visible in the device info)
3. **Home Assistant version** - Found in Settings → About
4. **Integration version** - Found in HACS or the manifest.json
5. **Steps to reproduce** - What actions led to the problem

### Bluetooth Debugging

For Bluetooth-specific issues, you may also want to enable debug logging for the Bluetooth integration:

```yaml
logger:
  default: info
  logs:
    custom_components.ideal_led: debug
    homeassistant.components.bluetooth: debug
    bleak: debug
```

> **Note:** Enabling `bleak` debug logging can produce a large volume of logs. Only enable it when specifically troubleshooting Bluetooth connectivity issues.

## Other projects that might be of interest

- [iDotMatrix](https://github.com/8none1/idotmatrix)
- [Zengge LEDnet WF](https://github.com/8none1/zengge_lednetwf)
- [iDealLED](https://github.com/8none1/idealLED)
- [BJ_LED](https://github.com/8none1/bj_led)
- [ELK BLEDOB](https://github.com/8none1/elk-bledob)
- [HiLighting LED](https://github.com/8none1/hilighting_homeassistant)
- [BLELED LED Lamp](https://github.com/8none1/ledble-ledlamp)

