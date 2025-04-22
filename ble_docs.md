# Template
## Bytes
|Nr.|Meaning|Allowed Values|Example|Ref|
|---|-------|--------------|-------|---|
|01|||||
|02|||||
|03|||||
|04|||||
|04|||||
|05|||||
|06|||||
|07|||||
|08|||||
|09|||||
|0a|||||
|0b|||||
|0c|||||
|0d|||||
|0e|||||
|0f|||||


# Mute Channel
## Bytes
|Nr.|Meaning|Allowed Values|Example|Ref|
|---|-------|--------------|-------|---|
|01|Length of Message|08|08||
|02|Unknown (Command?)|01|01||
|04|Channel|00…06|01|1|
|03|Mute/Unmute|00,01|00|2|

### Reference 01
|Channel|Byte|
|-------|----|
|1|00|
|2|01|
|3|02|
|4|03|
|5/6|04|
|7/8|05|
|BT|06|

### Reference 02
|Command|Byte|
|-------|----|
|Mute|01|
|Unmute|00|