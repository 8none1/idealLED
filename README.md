# iDeal LED control

![image](https://github.com/8none1/idealLED/assets/6552931/c5fcd8fc-440a-48dd-abe4-d6fdd2e4a422)

## Supported Features

- On / Off
- Set RGB colour of entire strip
- Set DIY LED patterns (not supported in Home Assistant)
- Set brightness
- Set effect
- Automatic discovery of supported devices in Home Assistant

## Not supported

- Discovery of current light state (no notifications from device)
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

## Warning

I have bricked one set of lights by sending invalid data to them while building this integration.  Use this repo at your own risk.
You should be careful when sending bytes to these lights which are outside of the already discovered values.

You can read more on this here: https://www.whizzy.org/2023-12-14-bricked-xmas/

As far as I can tell this integration does not use any unsafe values by default.  If you know otherwise, please open an issue, ideally with an accompanying PR.

## Other projects that might be of interest

- [iDotMatrix](https://github.com/8none1/idotmatrix)
- [Zengge LEDnet WF](https://github.com/8none1/zengge_lednetwf)
- [iDealLED](https://github.com/8none1/idealLED)
- [BJ_LED](https://github.com/8none1/bj_led)
- [ELK BLEDOB](https://github.com/8none1/elk-bledob)
- [HiLighting LED](https://github.com/8none1/hilighting_homeassistant)
- [BLELED LED Lamp](https://github.com/8none1/ledble-ledlamp)

