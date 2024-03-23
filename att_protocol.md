Notes:

LightStripBleSendData file looks useful

# Summary

```On  : ``` 
```Off : ```

# Initial on/off investigation

I followed the usual procedure as laid out [here](https://github.com/8none1/zengge_lednetwf#process)

- Wireshark filter for outgoing from Android to lights:  `(btatt or btgatt) && (btatt.opcode.method==0x12 || btatt.opcode.method==0x1b) && bluetooth.dst == 1a:b9:3a:2d:5e:63`

## on/off packet capture

```
0100
0100
21b0b6227d52f173accec8ab6854a092
263a91cc5f1bf003ce437b733478ada2
d12e61ad95a00bd3c56bee6f9cb545fe
18c59b941343e187299139e72516d7b6
79d1dba40919c246a8580ae7d11b7884
004ddd3127c7e4d7f950ea6cb240341e12
0270617373
01317940ef17e4d8c239ab8f83f11eba7e
fedcbac0030006abffffffff00ef
84dd5042374150897ac82f39110968a8
79d1dba40919c246a8580ae7d11b7884
84dd5042374150897ac82f39110968a8
79d1dba40919c246a8580ae7d11b7884
84dd5042374150897ac82f39110968a8
79d1dba40919c246a8580ae7d11b7884
84dd5042374150897ac82f39110968a8
```

The first thing I noticed is how much more chatty these lights are than others I have previously reverse engineered.  I hope these are not going to prove very difficult.
To start with I just turned the lights on and off a few times.  Let's see what we can spot.  There is at least a repeating pattern at the end which must be the on/off packets.

```
84 dd 50 42 37 41 50 89 7a c8 2f 39 11 09 68 a8
79 d1 db a4 09 19 c2 46 a8 58 0a e7 d1 1b 78 84
84 dd 50 42 37 41 50 89 7a c8 2f 39 11 09 68 a8
79 d1 db a4 09 19 c2 46 a8 58 0a e7 d1 1b 78 84
84 dd 50 42 37 41 50 89 7a c8 2f 39 11 09 68 a8
79 d1 db a4 09 19 c2 46 a8 58 0a e7 d1 1b 78 84
84 dd 50 42 37 41 50 89 7a c8 2f 39 11 09 68 a8
```

First the good news.  The packets are identical each time.  This suggests that there is not any packet counters, checksums or complicated encryption.
Why are the packets so busy though? 

We can test these with a simple replay test using gatttool. 

## Red, Green, Blue packet capture

```
0100
0100
002d3bd548ae44c6193a9d25a92e75f7ea
00ed59059e2147ec0a207052396b8f33e9
8d7f9a74f2d235b8271e6f8bc8ead3a7
263a91cc5f1bf003ce437b733478ada2
d12e61ad95a00bd3c56bee6f9cb545fe
18c59b941343e187299139e72516d7b6
2dec317e7181ccb079fc665ae43fa9dd
002d3bd548ae44c6193a9d25a92e75f7ea
7a3948dadea3c9e8b2c37c3c4b82894d
6bc5c60c25f6ee2749e01b143b5a8cf9
2dec317e7181ccb079fc665ae43fa9dd
7a3948dadea3c9e8b2c37c3c4b82894d
6bc5c60c25f6ee2749e01b143b5a8cf9
2dec317e7181ccb079fc665ae43fa9dd
7a3948dadea3c9e8b2c37c3c4b82894d
6bc5c60c25f6ee2749e01b143b5a8cf9
2dec317e7181ccb079fc665ae43fa9dd
7a3948dadea3c9e8b2c37c3c4b82894d
6bc5c60c25f6ee2749e01b143b5a8cf9
2dec317e7181ccb079fc665ae43fa9dd
7a3948dadea3c9e8b2c37c3c4b82894d
6bc5c60c25f6ee2749e01b143b5a8cf9
2dec317e7181ccb079fc665ae43fa9dd
7a3948dadea3c9e8b2c37c3c4b82894d
6bc5c60c25f6ee2749e01b143b5a8cf9
2dec317e7181ccb079fc665ae43fa9dd
7a3948dadea3c9e8b2c37c3c4b82894d
6bc5c60c25f6ee2749e01b143b5a8cf9
79d1dba40919c246a8580ae7d11b7884
```

This conversation involves starting the iDeal LED app, selecting the device, going in to DIY mode and setting the strip to red, then green, then blue, then red, then green, then blue etc.  Finally the strip is switched off.

The last packet in this list is recognisable as the `OFF` packet from the previous capture.  So we should look for a repeating pattern in the preceding packets.  Which we can indeed see.

Red:   `2d ec 31 7e 71 81 cc b0 79 fc 66 5a e4 3f a9 dd`
Green: `7a 39 48 da de a3 c9 e8 b2 c3 7c 3c 4b 82 89 4d`
Blue:  `6b c5 c6 0c 25 f6 ee 27 49 e0 1b 14 3b 5a 8c f9`

Wow.  This is way more complex than any other lights I've looked at.  What is going on here?

## Brightness
On off on off on, red (255,0,0) stuff, green(0,255,0), down, up, down up

```
0100
0100
79d1dba40919c246a8580ae7d11b7884
b587feaa11d1295eb94012dfb61f83cd
263a91cc5f1bf003ce437b733478ada2
00f608b7fe884734c8aa0621f9b288ac51
0270617373
01660f5d911e2c4a2407ccb2ec658c6d12
d12e61ad95a00bd3c56bee6f9cb545fe
fedcbac00300061affffffff00ef
18c59b941343e187299139e72516d7b6
79d1dba40919c246a8580ae7d11b7884
84dd5042374150897ac82f39110968a8
79d1dba40919c246a8580ae7d11b7884
84dd5042374150897ac82f39110968a8
8b296a0ee4da1e0fd1c1a7d5ded61643
9b446f8707620af4c31402b5a6ff51ab
ce650b3e519e99f17177c6cd6179f1f9
ce650b3e519e99f17177c6cd6179f1f9
ce650b3e519e99f17177c6cd6179f1f9
ce650b3e519e99f17177c6cd6179f1f9
4830c49aaa5c88a189475a1c57c4b323
4830c49aaa5c88a189475a1c57c4b323
4830c49aaa5c88a189475a1c57c4b323
4830c49aaa5c88a189475a1c57c4b323
4830c49aaa5c88a189475a1c57c4b323
4830c49aaa5c88a189475a1c57c4b323
33f4d9fd01029378ef6b3688877a9946
33f4d9fd01029378ef6b3688877a9946
33f4d9fd01029378ef6b3688877a9946
c187962b6703c480f3bcdebf14dffa98
c187962b6703c480f3bcdebf14dffa98
c187962b6703c480f3bcdebf14dffa98
c187962b6703c480f3bcdebf14dffa98
c187962b6703c480f3bcdebf14dffa98
9673244c0a8c32bb7ba4b65009897bd5
9673244c0a8c32bb7ba4b65009897bd5
[ deleted a load of numbers]
a0403c0a03d3527ca02459e4fceb92ab
a0403c0a03d3527ca02459e4fceb92ab
a0403c0a03d3527ca02459e4fceb92ab
4550ba47dbf0623d6babdd4d24d2efee
4550ba47dbf0623d6babdd4d24d2efee
5e86c20e237ef37a9e355629dcc044c9
5e86c20e237ef37a9e355629dcc044c9
aaacb31c7396a064fb29b087d15bfee8
aaacb31c7396a064fb29b087d15bfee8
8bc3478452f75b378d19090f6f858516
8bc3478452f75b378d19090f6f858516
10d29606b04d1763efb041483b99a948
10d29606b04d1763efb041483b99a948
f780eff04d6efafe3b4297af37712222
f780eff04d6efafe3b4297af37712222
b18b433cad9244a9d8ab5abc45b359b3
b18b433cad9244a9d8ab5abc45b359b3
bb81c6c78b850f04adc2132d05bdb20c
bb81c6c78b850f04adc2132d05bdb20c
f7c4a457d18f10b1e7f235955443cdb8
f7c4a457d18f10b1e7f235955443cdb8
f7c4a457d18f10b1e7f235955443cdb8
```

```
b1 8b 43 3c ad 92 44 a9 d8 ab 5a bc 45 b3 59 b3
b1 8b 43 3c ad 92 44 a9 d8 ab 5a bc 45 b3 59 b3
bb 81 c6 c7 8b 85 0f 04 ad c2 13 2d 05 bd b2 0c
bb 81 c6 c7 8b 85 0f 04 ad c2 13 2d 05 bd b2 0c
f7 c4 a4 57 d1 8f 10 b1 e7 f2 35 95 54 43 cd b8
f7 c4 a4 57 d1 8f 10 b1 e7 f2 35 95 54 43 cd b8
```


## Step back a moment

There is no reasoning these bytes, which suggests that the data is encrypted.
But, we know that the same command produces the same bytes - so the key can't be temporal.
Also from a bit of Googling I know that the bytes we have for "on" and "off" are the same bytes as one other [person who as tried this](https://github.com/koying/ha_ideal_led_ble).
That means that the key is fixed.

So we have some basic encryption at play, but not a very good one.  Time to break out `jadx`.

## Decompile the app

There is reference to AES encryption in here, and an external library is used to encrypt the payload.  (Side note: we should be able to decode the byte patterns to functions with the decompiled code.)
Let's see what the team think....  @sil found this page: https://habr.com/ru/articles/722412/
Run it through Google Translate and....  we have a key.  Let's assume the key is exactly the same, because it probably is.

```
    key = [
        0x34,
        0x52,
        0x2A,
        0x5B,
        0x7A,
        0x6E,
        0x49,
        0x2C,
        0x08,
        0x09,
        0x0A,
        0x9D,
        0x8D,
        0x2A,
        0x23,
        0xF8
    ]
```

This decodes the red, green and blue packets to:

`0x0F, 0x53, 0x47, 0x4C, 0x53, 0x00, 0x00, 0x64, 0x50, 0x1F, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x32`
`0x0F, 0x53, 0x47, 0x4C, 0x53, 0x00, 0x00, 0x64, 0x50, 0x00, 0x1F, 0x00, 0x00, 0x1F, 0x00, 0x32`
`0x0F, 0x53, 0x47, 0x4C, 0x53, 0x00, 0x00, 0x64, 0x50, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x1F, 0x32`

This looks encouraging.  The header is now fixed, and the bytes representing RGB look to be moving around as we would expect.
The only question now is why is it 0x1F and not 0xFF?
Maybe the key isn't right.  Let's check that aes library using IDA as our friend above did.
Loaded the file in to IDA, and the code is exactly the same and the key is the same.  So we have the correct key.

This is progress.

Now let's search the Android app for the header part of those decoded bytes: `0x0F, 0x53, 0x47`.  The decompiled app has everything in decimal, so we should search for:
`15, 83, 71`

Bingo!

```
byte[] bArr = {15, 83, 71, 76, 83, (byte) lightsColor.getModelIndex(), (byte) (1 ^ z), 100, (byte) lightsColor.getSpeed(), red, green, blue, red2, green2, blue2, (byte) lightsColor.getSaturation()};
```

So now we can decode the command bytes too.

More details are in the file `Source Code -> com -> tech -> idealled -> ble`

## Starting to understand the conversation

At this point I can understand the basic colour settings.  The device seems to use 5 bit colour, and as far as I can tell at the moment those RGB bytes are sent twice in the same packet.  I suspect that the second copy of those bytes is some kind of secondary colour for gradients, but I haven't tested it yet.

I've written a basic Python script to unencrypt the packets.

Before I start working on controlling more features of the light I want to understand the initialisation packets and the notifications.

I'm going to start with the packets that are sent at the start when opening the app.

This is a clear text start up procedure from the Android device to the lights:

```
0x15, 0x54, 0x49, 0x4D, 0x45, 0x02, 0x0D, 0x2D, 0x0A, 0xA5, 0x5A, 0xA5, 0x01, 0x02, 0x06, 0x09 - gets time
0x03, 0x56, 0x45, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 - get version
0x03, 0x56, 0x45, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 - get version as well?
0x0E, 0x43, 0x54, 0x01, 0x01, 0x00, 0x00, 0x64, 0x00, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
0x05, 0x54, 0x55, 0x52, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
```

The last command should be me turning it off.  Let's convert that to decimal and see if it's in the code:

5, 84, 85, 82, 78

We find:
```
    @Override // com.example.lightstrip.exposed.BleSendData
    public boolean switchLed(boolean z) {
        boolean write1 = LightStripBleManager.getInstance().write1(Agreement.getEncryptData(new byte[]{5, 84, 85, 82, 78, z ? (byte) 1 : (byte) 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}));
        LogUtil.d("进入开关灯模式：->>" + write1);
        return z;
    }
```

进入开关灯模式 translates as "Enter switch light mode".

So we can use the same method to try and work out what the first 4 things do:

21, 84, 73, 77, 69.... - sets the time `public static byte[] getTimeCommand(Context context, int i, int i2, int i3)`

3, 86, 69.... - get version ``` public static byte[] getVersion() {
        return new byte[]{3, 86, 69, 82, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    }```
There are two versions of this, one with byte 4 (starting at 1) as 0, and one with it being 1.  Perhaps this is to support different devices?

14, 67, 84... not sure.  Perhaps something to do with connection type, or perhaps the number of LEDs in the string?

5, 84, 85... off

I expect that the two unknowns are commands to get the lights to notify with a bunch of data about them so the app knows what is going on.

We will see.  I can change some of the settings in the app and see what happens if necessary.  My strip claims to be 10M long with 100 LEDs.

There is also some set up which I skipped over here which is setting up notifications.  I should be able to work that out without the app.

## Modes / effects

Let's try and work out some of the modes and effects this thing has...

Here are some effects changing commands:
```
0x0A, 0x4D, 0x55, 0x4C, 0x54, 0x07, 0x00, 0x64, 0x50, 0x07, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00
0x0A, 0x4D, 0x55, 0x4C, 0x54, 0x07, 0x00, 0x64, 0x50, 0x07, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00
0x0A, 0x4D, 0x55, 0x4C, 0x54, 0x07, 0x00, 0x64, 0x50, 0x07, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00
0x0A, 0x4D, 0x55, 0x4C, 0x54, 0x07, 0x00, 0x64, 0x50, 0x07, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00
0x0A, 0x4D, 0x55, 0x4C, 0x54, 0x08, 0x00, 0x64, 0x50, 0x07, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00
0x0A, 0x4D, 0x55, 0x4C, 0x54, 0x09, 0x00, 0x64, 0x50, 0x07, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00
0x0A, 0x4D, 0x55, 0x4C, 0x54, 0x00, 0x00, 0x64, 0x50, 0x07, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00
0x0A, 0x4D, 0x55, 0x4C, 0x54, 0x01, 0x00, 0x64, 0x50, 0x07, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00
0x0A, 0x4D, 0x55, 0x4C, 0x54, 0x02, 0x00, 0x64, 0x50, 0x07, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00
0x0A, 0x4D, 0x55, 0x4C, 0x54, 0x03, 0x00, 0x64, 0x50, 0x07, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00
```

There was also some data which couldn't be encrypted between these.  I think that the mode data itself is not encrypted.  Let's see.

We have a standard header, in decimal is: `10, 77, 85, 76, 84` - search for that in the app:

```
 public void sendMutilColor(BleDevice bleDevice, LightsColor lightsColor, AgreementListener agreementListener) {
        int modelIndex = lightsColor.getModelIndex();
        LogUtil.m104d("===index:" + modelIndex);
        if (bleDevice.getProductType() == 3) {
            switch (modelIndex) {
                case 10:
                    modelIndex = 17;
                    break;
                case 11:
                    modelIndex = 18;
                    break;
                case 12:
                    modelIndex = 19;
                    break;
                case 13:
                    modelIndex = 10;
                    break;
                case 14:
                    modelIndex = 11;
                    break;
                case 15:
                    modelIndex = 12;
                    break;
                case 16:
                    modelIndex = 13;
                    break;
                case 17:
                    modelIndex = 14;
                    break;
                case 18:
                    modelIndex = 15;
                    break;
                case 19:
                    modelIndex = 16;
                    break;
            }
        }
        StringBuilder sb = new StringBuilder();
        sb.append("发送多色效果：");
        sb.append(modelIndex - 10);
        LogUtil.m104d(sb.toString());
        byte[] bArr = {10, 77, 85, 76, 84, (byte) (((byte) modelIndex) - 10), (byte) (!((lightsColor.getSceneType() == 12 && modelIndex == 10) ? !lightsColor.isReverseState() : lightsColor.isReverseState())), 100, (byte) lightsColor.getSpeed(), (byte) lightsColor.getColorsArr().size(), (byte) lightsColor.getSaturation(), 0, 0, 0, 0, 0};
        LogUtil.m104d("发送多色效果数据命令：" + ByteUtils.BinaryToHexString(bArr));
        byte[] encryptData = Agreement.getEncryptData(bArr);
        ArrayList<Integer> colorsArr = lightsColor.getColorsArr();
        byte[] bArr2 = new byte[colorsArr.size() * 3];
        for (int i = 0; i < colorsArr.size(); i++) {
            int intValue = colorsArr.get(i).intValue();
            int red = Color.red(intValue);
            int green = Color.green(intValue);
            int blue = Color.blue(intValue);
            int i2 = i * 3;
            bArr2[i2] = (byte) ColorConverter.calculationByColour(red, lightsColor.getSaturation());
            bArr2[i2 + 1] = (byte) ColorConverter.calculationByColour(green, lightsColor.getSaturation());
            bArr2[i2 + 2] = (byte) ColorConverter.calculationByColour(blue, lightsColor.getSaturation());
        }
        this.dataMap.put(bleDevice, bArr2);
        this.listenerMap.put(bleDevice, agreementListener);
        LogUtil.m104d("发送多色效果结果 :" + BleManager.getInstance().write(bleDevice, encryptData));
    }
```

The dec. version of a payload looks like: `10, 77, 85, 76, 84, 3, 0, 100, 80, 7, 50, 0, 0, 0, 0, 0`

10 - header
77 - header
85 - header
76 - header
84 - header
3 - modelIndex minus 10 <== THIS IS THE ONLY ONE THAT CHANGES
0 - boolean if model = 10 and getSceneType=12 - might just be direction?
100 - fixed
80 - speed
7 - size of getColor array.  Need to look at the lightsColor class
50 - saturation
0 - footer
0 - footer
0 - footer
0 - footer
0 - footer


The packet which follows this one looks like:

`16007f06067f51007f7f00007f0000007f7f007f002b66000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000`

`16007f06067f51007f7f00007f0000007f7f007f002b66000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000`

`16007f06067f51007f7f00007f0000007f7f007f002b66000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000`

```
16 00 7f 06 06 7f 51 00 7f 7f 00 00 7f 00 00 00 7f 7f 00 7f 00 2b 66 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

These long numbers are unencrypted RRGGBB colours which then scroll down the string.  The first two bytes mean something, but I don't know what yet.
And now I do.  The first byte is how many bytes of colour data there are (increases by 3 for each new colour, i.e RR BB GG).  The second byte is (so far) always zero.

This pair:

unencrypted
`0A 4D 55 4C 54 07 01 64 50 06 64 00 00 00 00 00`

decrypted
```text
10 77 85 76 84 7 1 100 80 6 100 0 0 0 0 0
-------------- header
                         |- 6 = colour array size.  6 is 2x3?  i.e RRBBGG?
1300ffffffffffffff000007ff040002ffffffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
```


## 19 dec


## Initial chatter

Sets the time and stuff

Then this:

(decimal) `14, 67, 84, 1, 1, 0, 0, 100, 0, 100, 0, 0, 0, 0, 0, 0`

which doesn't seem to exist in the Android app.

??

## Effects

Going in to effects mode does this:
`21 84 73` - get time
`03 86 69` - get version pcb
`03 86 69` - get version fw
`14 67 84` - maybe some sorting thing?  (assuming set up LED colour byte ordering, not sure)
`10 77 85` - "multicolur"

`10 77 85 76 84 07 01 100 80 06 100 00 00 00 00 00`

```
        byte[] bArr = {10, 77, 85, 76, 84, (byte) (((byte) modelIndex) - 10), (byte) (!((lightsColor.getSceneType() == 12 && modelIndex == 10) ? !lightsColor.isReverseState() : lightsColor.isReverseState())), 100, (byte) lightsColor.getSpeed(), (byte) lightsColor.getColorsArr().size(), (byte) lightsColor.getSaturation(), 0, 0, 0, 0, 0};
```


```
                                     0  1  2  3  4  5  6  7   8  9  10  11 12 13 14 15
                                     10 77 85 76 84 07 01 100 80 06 100 00 00 00 00 00
header  -----------------------------|            | |  |  |   |  |  |   |           |
effect number --------------------------------------|  |  |   |  |  |   |           |
reverse? ----------------------------------------------|  |   |  |  |   |           |
fixed (led count?) ---------------------------------------|   |  |  |   |           |
speed --------------------------------------------------------|  |  |   |           |
colour array size? seems to be 6 all the time? ------------------|  |   |           |
saturation ---------------------------------------------------------|   |           |
always zero? -----------------------------------------------------------|-----------|

```

Then we send the big pixel array to the other end point (unencrypted)

```
13 00 FF FF FF FF FF FF FF 00 00 07 FF 04 00 02 FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```
first byte is the number of pixels being sent with a colour
0x13 = 19d and there are 19 pixels being sent
Also note these are now 8 bit colours, not 5 bit!?!


When cycling though effects (this is the string of lights on a house one, perhaps called "Light Post") we see this (decimal):
```
10 77 85 76 84 08 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 09 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 00 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 01 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 02 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 03 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 04 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 05 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 06 00 100 80 07 50 00 00 00 00 00
```

When we switch to another effect (Christmas tree):

```
10 77 85 76 84 08 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 09 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 00 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 01 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 02 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 03 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 04 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 05 00 100 80 07 50 00 00 00 00 00
10 77 85 76 84 06 00 100 80 07 50 00 00 00 00 00
```

The look the same to me.

The big array of colours looks like this:
```
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
16 00 7F 00 00 7F 51 00 7F 7F 00 00 7F 00 00 00 7F 7F 00 7F 7F 7F 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

These are all the same!

This suggest then that all the effects on this thing are the same like 10 effects.

There are 80 bytes in this list.  There are 100 LEDs. Go figure.



## Graffiti

Footer ----------------------------------------------------|| ||
Blue ---------------------------------------------------|| || ||
Green -----------------------------------------------|| || || ||
Red ----------------------------------------------|| || || || ||
Speed --------------------------------------------|| || || || ||
Mode ------------------------------------------|| || || || || ||
"Tuya light location?"-------------------||-|| || || || || || ||
LED number 0 to 100 dec --------------|| ||-|| || || || || || ||
Header           |------------------| || ||-|| || || || || || ||
                 0D 44 4F 4F 44 01 00 0A 02 64 07 FF 00 64 00 00




```
Decrypted:       0D 44 4F 4F 44 01 00 0A 02 64 07 FF 00 64 00 00
Decrypted:       0D 44 4F 4F 44 01 00 0B 02 64 07 FF 00 64 00 00
Decrypted:       0D 44 4F 4F 44 01 00 0C 02 64 07 FF 00 64 00 00
Decrypted:       0D 44 4F 4F 44 01 00 0D 02 64 07 FF 00 64 00 00
Decrypted:       0D 44 4F 4F 44 01 00 0E 02 64 07 FF 00 64 00 00
Decrypted:       0D 44 4F 4F 44 01 00 0F 02 64 07 FF 00 64 00 00
Decrypted:       0D 44 4F 4F 44 01 00 10 02 64 07 FF 00 64 00 00
Decrypted:       0D 44 4F 4F 44 01 00 11 02 64 07 FF 00 64 00 00
Decrypted:       0D 44 4F 4F 44 01 00 12 02 64 07 FF 00 64 00 00
Decrypted:       0D 44 4F 4F 44 01 00 13 02 64 07 FF 00 64 00 00
Decrypted:       0D 44 4F 4F 44 01 00 14 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 15 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 16 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 17 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 18 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 19 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 1A 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 1B 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 1C 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 47 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 44 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 33 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 30 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 1F 02 64 00 04 FC 63 00 00
Decrypted:       0D 44 4F 4F 44 01 00 63 02 64 FC 00 00 63 00 00
```

```
        public static void graffiti(final int i, final RGB rgb, final int i2) {
        ThreadUtils.async(new CallBack() { // from class: com.tech.smartlights.ble.BleProtocol.1
            @Override // com.heaton.baselib.callback.CallBack
            public void execute() {
                byte[] hex2byte = Convert.hex2byte(Convert.integerToHexString(i2));
                if (hex2byte.length < 2) {
                    hex2byte = new byte[]{0, hex2byte[0]};
                }
                float a = rgb.getA() / 255.0f;
                byte[] bArr = (rgb.getA() == 255 && rgb.getR() == 16 && rgb.getG() == 16 && rgb.getB() == 16) ? new byte[]
                {13, 68, 79, 79, 68, (byte) i, hex2byte[0], hex2byte[1], (byte) rgb.getMode(), (byte) rgb.getSpeed(), (byte) (rgb.getR() * 0.0f), (byte) (rgb.getG() * 0.0f), (byte) (rgb.getB() * 0.0f), (byte) DataManager.getInstance().getDiyLight(), 0, 0} : new byte[]{13, 68, 79, 79, 68, (byte) i, hex2byte[0], hex2byte[1], (byte) rgb.getMode(), (byte) rgb.getSpeed(), (byte) (rgb.getR() * a), (byte) (rgb.getG() * a), (byte) (rgb.getB() * a), (byte) DataManager.getInstance().getDiyLight(), 0, 0};
                LogUtil.m104d("发送涂鸦数据" + ByteUtils.BinaryToHexString(bArr));
                LogUtil.m104d("发送涂鸦数据灯位置：--》" + i2);
                boolean writeAll = BleManager.getInstance().writeAll(Agreement.getEncryptData(bArr), DataManager.getInstance().getProductType());
                LogUtil.m104d("发送涂鸦数据result:" + writeAll);
            }
        });
```


in to graf mode (cleared everything)
first px red
last blue
flood fill green
flood fill red
erase last
erase first
delete all

```

Footer ----------------------------------------------------|| ||
Blue ---------------------------------------------------|| || ||
Green -----------------------------------------------|| || || ||
Red ----------------------------------------------|| || || || ||
Speed --------------------------------------------|| || || || ||
Mode ------------------------------------------|| || || || || ||
"Tuya light location?"-------------------||-|| || || || || || ||
LED number 0 to 100 dec --------------|| ||-|| || || || || || ||
Header           |------------------| || ||-|| || || || || || ||
                 15 54 49 4D 45 04 0A 2E 2F A5 5A A5 01 02 06 09
                 03 56 45 00 00 00 00 00 00 00 00 00 00 00 00 00
                 03 56 45 01 00 00 00 00 00 00 00 00 00 00 00 00
                 0E 43 54 01 01 00 00 64 00 64 00 00 00 00 00 00
                 04 44 45 4E 00 00 00 00 00 00 00 00 00 00 00 00 - maybe cleared?
                 0D 44 4F 4F 44 01 00 00 02 64 FC 00 00 63 00 00 - first px red
                 0D 44 4F 4F 44 01 00 63 02 64 00 43 FC 63 00 00 - last px blue (0x63 is last px)
                 0D 44 4F 4F 44 00 00 64 02 64 25 FF 00 64 00 00 - flood?  yes - pixel 64 is "all"
                 0D 44 4F 4F 44 00 00 64 02 64 25 FF 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 22 FF 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 3C FF 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 D3 FF 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 FF 65 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 63 02 64 00 00 00 64 00 00 - erase just sets colour to black
                 0D 44 4F 4F 44 01 00 00 02 64 00 00 00 64 00 00
                 0D 44 4F 4F 44 00 00 64 02 64 00 00 00 64 00 00 - and setting 64 to black clears the lot. Looks like the header might have changed slightly too

                 0D 44 4F 4F 44 01 00 00 02 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 01 01 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 02 01 32 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 03 01 19 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 04 00 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 05 00 31 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 06 00 19 FF 00 00 64 00 00
header-----------|            | || || || || || ||
?                               || || || || || ||
0                                  || || || || ||
pixel                                 || || || ||
mode 02 solid, 01 fade 02 flash          || || ||
speed 0-100dec -----------------------------|| ||  ||                                                               
red                                            ||
green                                             ||
blue                                                 ||
brightness                                              ||
footer                                                     || ||

                 0D 44 4F 4F 44 01 00 00 02 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 00 02 64 10 FF 00 64 00 00
                 0D 44 4F 4F 44 01 00 00 02 64 00 50 FF 64 00 00
                 0D 44 4F 4F 44 01 00 01 01 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 01 01 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 02 01 64 24 FF 00 64 00 00
                 0D 44 4F 4F 44 01 00 03 01 64 00 3C FF 64 00 00
                 0D 44 4F 4F 44 01 00 04 01 32 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 05 01 32 1F FF 00 64 00 00
                 0D 44 4F 4F 44 01 00 06 01 32 00 3C FF 64 00 00
                 0D 44 4F 4F 44 01 00 07 01 19 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 08 01 19 22 FF 00 64 00 00
                 0D 44 4F 4F 44 01 00 09 01 19 00 44 FF 64 00 00
                 0D 44 4F 4F 44 01 00 13 00 64 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 12 00 64 2D FF 00 64 00 00
                 0D 44 4F 4F 44 01 00 11 00 64 00 26 FF 64 00 00
                 0D 44 4F 4F 44 01 00 10 00 32 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 0F 00 32 01 FF 00 64 00 00
                 0D 44 4F 4F 44 01 00 0E 00 32 00 1E FF 64 00 00
                 0D 44 4F 4F 44 01 00 0D 00 19 FF 00 00 64 00 00
                 0D 44 4F 4F 44 01 00 0C 00 19 04 FF 00 64 00 00
                 0D 44 4F 4F 44 01 00 0B 00 19 00 32 FF 64 00 00

```

