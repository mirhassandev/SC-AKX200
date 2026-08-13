# Panasonic Maxjuke Remote Control & Sound Settings - Code Reference

**Last Updated:** 2026-08-13  
**Sources:** `sources/com/panasonic/avc/diga/maxjuke/menu/remocon/`

---

## 1. REMOTE CONTROL BUTTON CODES (RemoconButtonItem Enum)

### Core Navigation & Power
| Button | Enum Name | Primary Payload | Type | File |
|--------|-----------|-----------------|------|------|
| Power | `REMOCON_CODE_POWER` | `{28, 61}` | Single | RemoconButtonItem:7 |
| OK | `REMOCON_CODE_OK` | `{28, -5}` | Single | RemoconButtonItem:50 |
| Left | `REMOCON_CODE_LEFT` | `{28, -3}` | Long-press | RemoconButtonItem:46 |
| Right | `REMOCON_CODE_RIGHT` | `{28, -4}` | Long-press | RemoconButtonItem:47 |
| Up | `REMOCON_CODE_UP` | `{28, -13}` | Long-press | RemoconButtonItem:48 |
| Down | `REMOCON_CODE_DOWN` | `{28, -14}` | Long-press | RemoconButtonItem:49 |

### Volume & Mute
| Button | Enum Name | Primary Payload | Type | File |
|--------|-----------|-----------------|------|------|
| Volume Up | `REMOCON_CODE_VOLUME_UP` | `{0, 32}` | Long-press | RemoconButtonItem:27 |
| Volume Down | `REMOCON_CODE_VOLUME_DOWN` | `{0, 33}` | Long-press | RemoconButtonItem:28 |
| Mute | `REMOCON_CODE_MUTE` | `{0, 50}` | Single | RemoconButtonItem:29 |

### Selectors
| Button | Enum Name | Payload (UA30) | Type | File |
|--------|-----------|----------------|------|------|
| Select Up | `REMOCON_CODE_SELECT_UP` | `{28, -122}` | Single | RemoconButtonItem:84 |
| Select Down | `REMOCON_CODE_SELECT_DOWN` | `{28, -121}` | Single | RemoconButtonItem:83 |

### Playback Control
| Button | Enum Name | Primary Payload | Type | File |
|--------|-----------|-----------------|------|------|
| Play/Pause | `REMOCON_CODE_PLAY_PAUSE` | `{28, 6}` | Single | RemoconButtonItem:38 |
| Stop | `REMOCON_CODE_STOP` | `{28, 0}` | Single | RemoconButtonItem:39 |
| Skip Rewind | `REMOCON_CODE_SKIP_REW` | `{28, 73}` | Long-press | RemoconButtonItem:34 |
| Skip Forward | `REMOCON_CODE_SKIP_FWD` | `{28, 74}` | Long-press | RemoconButtonItem:35 |
| Search Rewind | `REMOCON_CODE_SEARCH_REW` | `{28, 2}` | Long-press | RemoconButtonItem:36 |
| Search Forward | `REMOCON_CODE_SEARCH_FWD` | `{28, 3}` | Long-press | RemoconButtonItem:37 |

### Sound & Audio Modes
| Button | Enum Name | Primary Payload | Type | File |
|--------|-----------|-----------------|------|------|
| Sound Menu | `REMOCON_CODE_SOUND` | `{20, -80}` | Single | RemoconButtonItem:41 |
| Preset EQ | `REMOCON_CODE_PRESET_EQ` | `{16, -125}` | Single | RemoconButtonItem:40 |
| D.Bass | `REMOCON_CODE_D_BASS` | `{0, -55}` (Type 1) | Single | RemoconButtonItem:43 |
| Manual EQ | `REMOCON_CODE_EQ` | `{0, -40}` | Single | RemoconButtonItem:79 |

### Numeric & Selection
| Button | Enum Name | Payload | File |
|--------|-----------|---------|------|
| 0 | `REMOCON_CODE_0` | `{28, 25}` | RemoconButtonItem:23 |
| 1 | `REMOCON_CODE_1` | `{28, 16}` | RemoconButtonItem:14 |
| 2 | `REMOCON_CODE_2` | `{28, 17}` | RemoconButtonItem:15 |
| 3 | `REMOCON_CODE_3` | `{28, 18}` | RemoconButtonItem:16 |
| 4 | `REMOCON_CODE_4` | `{28, 19}` | RemoconButtonItem:17 |
| 5 | `REMOCON_CODE_5` | `{28, 20}` | RemoconButtonItem:18 |
| 6 | `REMOCON_CODE_6` | `{28, 21}` | RemoconButtonItem:19 |
| 7 | `REMOCON_CODE_7` | `{28, 22}` | RemoconButtonItem:20 |
| 8 | `REMOCON_CODE_8` | `{28, 23}` | RemoconButtonItem:21 |
| 9 | `REMOCON_CODE_9` | `{28, 24}` | RemoconButtonItem:22 |
| 10 | `REMOCON_CODE_10` | `{28, -124}` | RemoconButtonItem:24 |

### Recording & Recording Modes
| Button | Enum Name | Primary Payload | Type | File |
|--------|-----------|-----------------|------|------|
| USB Record | `REMOCON_CODE_USB_REC` | `{28, -52}` (main); `{28, -51}` (shift) | Shift | RemoconButtonItem:54 |
| Memory Record | `REMOCON_CODE_MEMORY_REC` | `{28, -55}` (main); `{28, -54}` (shift) | Shift | RemoconButtonItem:55 |
| Rec Mode | `REMOCON_CODE_REC_MODE` | `{28, -65}` | Single | RemoconButtonItem:56 |
| Edit Mode | `REMOCON_CODE_EDIT_MODE` | `{28, -43}` | Single | RemoconButtonItem:52 |

### Source/Input Selection
| Button | Enum Name | Payload (Type varies) | File |
|--------|-----------|----------------------|------|
| USB | `REMOCON_CODE_USB` | `{28, -53}` (default); `{0, -124}` (UA7/Max) | RemoconButtonItem:31 |
| CD | `REMOCON_CODE_CD` | `{10, 10}` (default); `{0, -108}` (UA7) | RemoconButtonItem:32 |
| Bluetooth | `REMOCON_CODE_BLUETOOTH` | `{0, -91}` (UA7+) | RemoconButtonItem:59 |
| Aux | `REMOCON_CODE_AUX` | `{0, -102}` (CMAX5) | RemoconButtonItem:65 |
| Radio/Exit In | `REMOCON_CODE_RADIO_EXITIN` | `{4, -92}` | RemoconButtonItem:33 |

### Display & Menu
| Button | Enum Name | Payload (Type varies) | File |
|--------|-----------|----------------------|------|
| Display | `REMOCON_CODE_DISPLAY` | `{28, 85}` (UA7+) | RemoconButtonItem:64 |
| Display Dimmer | `REMOCON_CODE_DISPLAY_DIMMER` | `{28, 85}` | RemoconButtonItem:51 |
| Play Menu | `REMOCON_CODE_PLAY_MENU` | `{10, -69}` (default); `{28, -69}` (UA7+) | RemoconButtonItem:44 |
| Setup | `REMOCON_CODE_SETUP` | `{28, -75}` (UA7+) | RemoconButtonItem:63 |

### Additional Controls
| Button | Enum Name | Payload (Type varies) | File |
|--------|-----------|----------------------|------|
| Sleep | `REMOCON_CODE_SLEEP` | `{28, -106}` | RemoconButtonItem:9 |
| Auto Preset | `REMOCON_CODE_AUTO_PRESET` | `{4, -89}` (UA7+) | RemoconButtonItem:81 |
| Mic Vol | `REMOCON_CODE_MIC_VOL` | `{20, -39}` (UA7+) | RemoconButtonItem:82 |
| DJ Mode | `REMOCON_CODE_DJ` | `{28, -77}` (Max3500P+) | RemoconButtonItem:85 |

---

## 2. VOLUME, D.BASS & D.BASS BEAT CONSTANTS

### Source: RetSoundSet.java (Result codes from device response)

#### D.Bass Levels
```
RESULT_DBASS_OFF    = 0
RESULT_DBASS_ONE    = 1
RESULT_DBASS_TWO    = 2
RESULT_DBASS_THREE  = 3
RESULT_DBASS_FOUR   = 4
RESULT_DBASS_FIVE   = 5
RESULT_DBASS_SIX    = 6
```

#### D.Bass Beat
```
RESULT_DBASS_BEAT_OFF = 0
RESULT_DBASS_BEAT_ON  = 1
```

#### Manual EQ Levels (Bass, Mid, Treble)
```
RESULT_LEVEL_MINUS_FOUR  = 0  (-4)
RESULT_LEVEL_MINUS_THREE = 1  (-3)
RESULT_LEVEL_MINUS_TWO   = 2  (-2)
RESULT_LEVEL_MINUS_ONE   = 3  (-1)
RESULT_LEVEL_ZERO        = 4  (0)
RESULT_LEVEL_PLUS_ONE    = 5  (+1)
RESULT_LEVEL_PLUS_TWO    = 6  (+2)
RESULT_LEVEL_PLUS_THREE  = 7  (+3)
RESULT_LEVEL_PLUS_FOUR   = 8  (+4)
```

#### Surround
```
RESULT_SOURROUND_OFF = 0
RESULT_SOURROUND_ON  = 1
```

---

## 3. PRESET EQ MODES

### Source: RetSoundSet.java (Result codes) & SoundControlRemocon.java (Type definitions)

#### Preset EQ Mode Constants (values returned by device in `RetSoundSet.getPreset()`)
```
RESULT_PRESET_HEAVY         = 0
RESULT_PRESET_SOFT          = 1
RESULT_PRESET_CLEAR         = 2
RESULT_PRESET_VOCAL         = 3
RESULT_PRESET_FLAT          = 4
RESULT_PRESET_ROCK          = 5
RESULT_PRESET_POP           = 6
RESULT_PRESET_AFRO_BEAT     = 7
RESULT_PRESET_ARABIC        = 8
RESULT_PRESET_PERSIAN       = 9
RESULT_PRESET_INDIA_BASS    = 10
RESULT_PRESET_DANGDUT       = 11
RESULT_PRESET_MALAY_POP     = 12
RESULT_PRESET_ELECTRONICA   = 13
RESULT_PRESET_REGGAETON     = 14
RESULT_PRESET_SALSA         = 15
RESULT_PRESET_SAMBA         = 16
RESULT_PRESET_CUMBIA        = 17
RESULT_PRESET_FORRO         = 18
RESULT_PRESET_FUNK          = 19
RESULT_PRESET_SERTANEIO     = 20
RESULT_PRESET_AZE           = 21
RESULT_PRESET_MPB           = 22
RESULT_PRESET_FOOTBALL      = 23
RESULT_PRESET_KARAOKE       = 24
RESULT_PRESET_VOICE_EX1     = 25
RESULT_PRESET_MUSIC         = 26
RESULT_PRESET_BGM           = 27
RESULT_PRESET_CINEMA        = 28
RESULT_PRESET_NIGHT         = 29
RESULT_PRESET_SPORTS        = 30
RESULT_PRESET_TV            = 31
RESULT_PRESET_STANDARD      = 32
```

#### Preset EQ Type Definitions (SoundControlRemocon.PRESET_EQ_TYPE_*)
Used to determine which preset modes are supported per device model.

```
PRESET_EQ_TYPE_SMALL            = 0  (Heavy, Soft, Clear, Vocal, Flat)
PRESET_EQ_TYPE_LATIN            = 1  (Rock, Pop, etc. - Latin American set)
PRESET_EQ_TYPE_LOCAL            = 2  (Rock, Pop, etc. - Local set)
PRESET_EQ_TYPE_LOCAL_KARAOKE    = 3  (Local set + Karaoke)
PRESET_EQ_TYPE_LATIN_KARAOKE    = 4  (Latin set + Karaoke)
PRESET_EQ_TYPE_LOCAL_VOICE_EX   = 5  (Local set + Voice EX)
PRESET_EQ_TYPE_LATIN_VOICE_EX   = 6  (Latin set + Voice EX)
PRESET_EQ_TYPE_CMAX             = 7  (CMAX-specific modes)
PRESET_EQ_TYPE_UA7_JPN          = 8  (UA7 Japan-specific modes)
PRESET_EQ_TYPE_9                = 9  (Extended set - 30 preset modes)
PRESET_EQ_TYPE_10               = 10 (Extended set variant)
PRESET_EQ_TYPE_11               = 11 (Newest extended set - 32+ presets)
```

#### EQ Default Focus (determined by model/region in SoundControlRemocon constructor)
```
PRESET_EQ_FOCUS_FLAT     = 0  (Default: Flat mode)
PRESET_EQ_FOCUS_HEAVY    = 1  (Default: Heavy mode)
PRESET_EQ_FOCUS_MALAYPOP = 2  (Default: Malay Pop mode)
PRESET_EQ_FOCUS_ROCK     = 3  (Default: Rock mode)
PRESET_EQ_FOCUS_MUSIC    = 4  (Default: Music mode)
```

---

## 4. MANUAL EQ REMOTE CODES

### Source: ManualEQFragment.java

**Code Table Format:** Organized as `[index][level]` where index = 0 (Bass), 1 (Mid), 2 (Treble)

#### Bass Remote Codes (9 levels: -4 to +4)
```
Level -4: {1, 8}
Level -3: {1, 7}
Level -2: {1, 6}
Level -1: {1, 5}
Level  0: {1, 4}  ← Center
Level +1: {1, 3}
Level +2: {1, 2}
Level +3: {1, 1}
Level +4: {1, 0}
```

#### Mid Remote Codes (9 levels: -4 to +4)
```
Level -4: {1, 17}
Level -3: {1, 16}
Level -2: {1, 15}
Level -1: {1, 14}
Level  0: {1, 13}  ← Center
Level +1: {1, 12}
Level +2: {1, 11}
Level +3: {1, 10}
Level +4: {1, 9}
```

#### Treble Remote Codes (9 levels: -4 to +4)
```
Level -4: {1, 26}
Level -3: {1, 25}
Level -2: {1, 24}
Level -1: {1, 23}
Level  0: {1, 22}  ← Center
Level +1: {1, 21}
Level +2: {1, 20}
Level +3: {1, 19}
Level +4: {1, 18}
```

#### Surround Remote Codes
```
Surround ON:  {1, 27}
Surround OFF: {1, 28}
```

---

## 5. COMMAND & PROTOCOL IDs

### Bluetooth/SPP Command Codes
Used when sending remote codes or audio control commands to the device.

| Command | ID | Purpose | File |
|---------|-----|---------|------|
| **sendByteSpp(7, payload)** | 7 | Legacy remocon IR code transmission | Type2RemoconFragment, VolumeControlFragment, DbassFragment, PresetEQFragment |
| **sendByteSpp(40, array[])** | 40 | New BT-module volume protocol (array format: `[1, volume_value, flag]`) | Type2RemoconFragment, VolumeControlFragment |

#### Command Message IDs (Handler)
From `MaxBluetoothManagerService` and `RetData`:

```
COMMAND_ID_NotifyMainUnitSetting = (varies per implementation)
COMMAND_ID_GetSoundSet           = 148 (used in handlers to identify soundset responses)
```

---

## 6. SOUND SETTINGS PACKET LAYOUT

### Source: RetSoundSet.setupData(byte[] bArr)

Audio settings are read from the device response packet:

```
Byte Index | Field           | Type | Range/Notes
-----------|-----------------|------|--------------------
4          | Bass            | byte | 0-8 (RESULT_LEVEL_*)
5          | Mid/Treble      | byte | 0-8 (RESULT_LEVEL_*)
6          | Treble          | byte | 0-8 (RESULT_LEVEL_*)
7          | Preset EQ       | byte | 0-32 (RESULT_PRESET_*)
8          | Master Volume   | byte | 0-50 (volume level)
9          | Surround        | byte | 0-1 (OFF/ON)
10         | D.Bass          | byte | 0-6 (RESULT_DBASS_*)
11         | D.Bass Beat     | byte | 0-1 (OFF/ON)
```

---

## 7. REMOCON TYPE CONSTANTS

### Source: Remocon.java

Device-specific remote type mappings:

```
REMOCON_TYPE_MAX770_370_170_AKX78_58_38 = 0
REMOCON_TYPE_MAX670_AKX79                = 1
REMOCON_TYPE_AKX18                       = 2
REMOCON_TYPE_CMAX5                       = 3
REMOCON_TYPE_VKX95_65_25                 = 4
REMOCON_TYPE_MAX8000_6000_4000_AKX800... = 5
REMOCON_TYPE_MAX8700                     = 6
REMOCON_TYPE_UA7                         = 7
REMOCON_TYPE_UA7_P                       = 8
REMOCON_TYPE_AKX100                      = 9
REMOCON_TYPE_UA3_4                       = 10
REMOCON_TYPE_UA3_4_OTHER                 = 11
REMOCON_TYPE_CMAX                        = 12
REMOCON_TYPE_UA7_JPN                     = 13
REMOCON_TYPE_AKX910                      = 14
REMOCON_TYPE_MAX3500_P                   = 15
REMOCON_TYPE_UA30                        = 16
REMOCON_TYPE_UA30_OTHER                  = 17
```

---

## 8. KEY FILE LOCATIONS

| Purpose | File Path |
|---------|-----------|
| Remote Button Enum (all codes/payloads) | `sources/com/panasonic/avc/diga/maxjuke/menu/remocon/RemoconButtonItem.java` |
| Remote Type Definitions | `sources/com/panasonic/avc/diga/maxjuke/menu/remocon/Remocon.java` |
| Sound/EQ Settings & Type Defs | `sources/com/panasonic/avc/diga/maxjuke/menu/remocon/SoundControlRemocon.java` |
| Sound Settings Response Format | `sources/com/panasonic/avc/diga/maxjuke/bluetooth/retdata/RetSoundSet.java` |
| Manual EQ Remote Codes | `sources/com/panasonic/avc/diga/maxjuke/menu/remocon/ManualEQFragment.java` |
| D.Bass UI & Control | `sources/com/panasonic/avc/diga/maxjuke/menu/remocon/DbassFragment.java` |
| Preset EQ UI & Control | `sources/com/panasonic/avc/diga/maxjuke/menu/remocon/PresetEQFragment.java` |
| Volume Control (Type 1) | `sources/com/panasonic/avc/diga/maxjuke/menu/remocon/VolumeControlFragment.java` |
| Volume Control (Type 2) | `sources/com/panasonic/avc/diga/maxjuke/menu/remocon/Type2RemoconFragment.java` |
| Model Capability Checks | `sources/com/panasonic/avc/diga/maxjuke/util/CheckModelUtil.java` |

---

## 9. QUICK REFERENCE: MOST USED CODES

### Core Remote
- **Power:** `{28, 61}`
- **Vol Up:** `{0, 32}`
- **Vol Down:** `{0, 33}`
- **Mute:** `{0, 50}`
- **OK:** `{28, -5}`

### Sound Modes
- **Preset EQ Button:** `{16, -125}`
- **Manual EQ Button:** `{0, -40}`
- **D.Bass Button:** `{0, -55}` or `{0, -39}` (type-dependent)
- **Sound Menu:** `{20, -80}`

### Playback
- **Play/Pause:** `{28, 6}`
- **Stop:** `{28, 0}`
- **Skip Prev:** `{28, 73}`
- **Skip Next:** `{28, 74}`

### Protocol
- Send remocon codes: `sendByteSpp(7, payload)`
- New BT volume: `sendByteSpp(40, {1, volume, flag})`

