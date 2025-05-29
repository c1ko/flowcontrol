# flowcontrol
Reverse engineering BLE controls for the Behringer Flow 8 digital mixer.
This project is suspended but I wanted to share my work so far. Feel free to pick it up.

## Handshake
Take a look into flowcontrol.py to understand the handshake process.

## Mute Channel
|Nr.|Meaning|Example|Ref|
|---|-------|-------|---|
|01|Unknown|08|
|02|Unknown|01|
|03|Channel|01|1|
|04|Mute/Unmute|00|2|
|05|Checksum|0a|3|

## Channel Volume
|Nr.|Meaning|Example|Ref|
|---|-------|-------|---|
|01|Unknown|06|
|02|Unknown|01|
|03|Channel|00|1|
|04|Layer|0f|4|
|04|Volume|4c|
|05|Checksum|62|3|

## Switch Layer
For mute commands, the layer is not transmitted in the packet. Instead, the mixer is set to a certain layer when switching the layer in the app.

    Unknown           Layer  Unknown Checksum
    --------------------VV--------------VV
    21010840414243c4c5c6cf0000000b00000059 (Main Layer)
    21010840414243c4c5c6cc0000000b00000056 (FX1)
    21010840414243c4c5c6cd0000000b00000057 (FX2)
    21010840414243c4c5c64a0000000b000000d4 (Monitor 1)
    21010840414243c4c5c64b0000000b000000d5 (Monitor 2)

## References
### Reference 01
|Channel|Byte|Comment|
|-------|----|-------|
|1|00|
|2|01|
|3|02|
|4|03|
|5/6|04|
|7/8|05|
|BT|06|
|Main Out|0f|Only for fader volume|

### Reference 02
|Command|Byte|
|-------|----|
|Mute|01|
|Unmute|00|

### Reference 03
The checksum is a sum of all bytes in the packet, rolling over at ff.

### Reference 04
|Layer|Byte|
|-------|----|
|Main|0f|
|Monitor 1|0a|
|Monitor 2|0b|
|FX1|0c|
|FX2|0d|
