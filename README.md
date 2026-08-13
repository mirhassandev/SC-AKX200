# SC-AKX200 Control Panel

A professional, feature-rich desktop application for controlling Panasonic SC-AKX200 audio systems via Bluetooth SPP (Serial Port Profile) protocol. Provides comprehensive remote control functionality with advanced EQ management, D.Bass control, preset audio modes, and real-time system monitoring.

![SC-AKX200 Control Panel](Guillendesign-Variations-3-Music.ico)

## ✨ Features

### Remote Control
- **20+ Remote Control Buttons**: Power, Dimmer, Eject, Bluetooth, USB/CD, Aux, Rewind, Play, Forward, Stop
- **Audio Controls**: Volume Up/Down, Mute, Display, Sound Mode, Setup, Menu Navigation
- **Playback Control**: Full transport controls with visual feedback
- **Responsive Buttons**: Hover effects, bounce animations, and professional dark UI

### Audio Control
- **14 Preset EQ Modes**:
  - Rock, Pop, Electronica, Reggaeton, Cumbia, Salsa, Forro, Funk, Samba, Sertanejo, Axe, MPB, Football, Flat
  - One-click selection with visual feedback
  
- **Manual EQ Control**:
  - Bass slider (9 positions: -6 to +6)
  - Mid slider (9 positions: -6 to +6)
  - Treble slider (9 positions: -6 to +6)
  - Surround mode toggle (On/Off)
  
- **D.Bass System**:
  - 6 intensity levels (1-6) + Off option
  - Beat Sync toggle (On/Off for synchronized bass boost)

### System Features
- **Real-time Connection Status**: Shows device connection state (Online/Offline)
- **Port Selection**: Dropdown to select Bluetooth COM port
- **Port Persistence**: Remembers last used port
- **Debug Panel**: Frame Tester for manual payload validation (Ctrl+Shift+I)
- **Dark Professional UI**: Apple-adjacent color scheme with smooth 200ms transitions

## 🔧 Technical Specifications

### SPP Protocol Implementation
- **Frame Format**: `[0xAA (magic) | CMD_ID | LenHI | LenLO | ...payload... | Checksum]`
- **Checksum**: Two's complement calculation
- **Baud Rate**: 9600, 8N1
- **Command Types**:
  - `0x07`: Remote Control IR (Remocon)
  - `0x28`: Volume Control
  - `0x0A`: Sound Settings

### Technology Stack
- **Language**: Python 3.14+
- **UI Framework**: Flet 0.86.5
- **Serial Communication**: PySerial 3.5
- **Architecture**: Multi-threaded with asyncio event loop

## 📋 Requirements

- **Windows 10/11** (64-bit)
- **Python 3.14+** (automatically installed with Inno Setup installer)
- **Bluetooth adapter** with SPP support
- **Panasonic SC-AKX200** audio system

## 🚀 Installation

### Option 1: Installer (Recommended for Users)
1. Download `SC-AKX200-Setup.exe` from Releases
2. Run the installer with Admin privileges
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

**Features**:
- ✅ Automatic Python dependency installation
- ✅ No console windows or scary prompts
- ✅ Professional custom icon everywhere
- ✅ One-click uninstall

### Option 2: Manual Installation (for Developers)

```powershell
# Clone the repository
git clone https://github.com/yourusername/SC-AKX200.git
cd SC-AKX200

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the application
python panasonic_akx200_control.py
```

## 📖 Usage

### Getting Started
1. **Connect Your Device**:
   - Pair SC-AKX200 with your Windows machine via Bluetooth
   - Note the COM port assigned by Windows

2. **Launch the Application**:
   - Run `SC-AKX200.exe` (from installer) or `python panasonic_akx200_control.py`
   - Select the correct COM port from the dropdown
   - Click **Connect**

3. **Control Your System**:
   - Click buttons to send remote commands
   - Use tabs to switch between control modes
   - Monitor connection status in the UI

### Remote Control Tab
- Top row: Power, Dimmer, Eject, Bluetooth, USB/CD, Aux, Rewind, Play, Forward, Stop
- Bottom row: Volume Down, Volume Up, Setup, Mute, Display, Sound, Menu, Left, OK, Right

### Preset EQ Tab
- Click any EQ mode pill to activate it
- Selected mode highlighted in blue
- Real-time device update

### Manual EQ Tab
- Drag sliders to adjust Bass, Mid, Treble (-6 to +6)
- Toggle Surround mode on/off
- Live feedback from device

### D.Bass Tab
- Select intensity level (Off, 1-6)
- Toggle Beat Sync for synchronized bass
- Visual mode indicators

### Debug Features
- **Frame Tester**: Manually enter CH and CODE values to test payloads
- **Live Log**: Shows all sent/received frames with timestamps
- **Toggle**: Press `Ctrl+Shift+I` to show/hide debug panel

## 🏗️ Project Structure

```
SC-AKX200/
├── panasonic_akx200_control.py       # Main application (1100+ lines)
├── SC-AKX200-Setup.iss               # Inno Setup installer script
├── SC-AKX200.bat                     # Batch launcher
├── SC-AKX200.vbs                     # VBScript silent runner
├── install_deps.py                   # Silent dependency installer
├── requirements.txt                  # Python dependencies
├── Guillendesign-Variations-3-Music.ico  # Application icon
├── wizard.bmp                        # Installer wizard image
├── PROTOCOL_FIX_SUMMARY.md           # SPP protocol documentation
├── REMOTE_SOUND_CODES_REFERENCE.md   # Command payload reference
└── README.md                         # This file
```

## 🔌 Bluetooth Connection Setup

### Windows Bluetooth Pairing
1. Settings → Bluetooth & devices → Add device
2. Select "Bluetooth"
3. Search for "SC-AKX200"
4. Complete pairing process
5. Open Device Manager to find COM port:
   - Search "devmgmt.msc"
   - Expand "Ports (COM & LPT)"
   - Note the COM port for SC-AKX200

### Troubleshooting Connection
- Ensure device is powered on and in Bluetooth discovery mode
- Check COM port is correct in dropdown
- Verify PySerial can access the port
- Try different baud rates if connection fails

## 🔄 Command Protocol

### Remote Control Payload Format
```
Remocon Command:
[CH, CODE]

Examples:
Power:     [28, 61]
Bluetooth: [0, -91]
Volume+:   [0, 32]
Volume-:   [0, 33]
Mute:      [0, 50]
Sound:     [20, -80]
```

### Frame Structure
```
AA 07 [LenHI] [LenLO] [Payload...] [Checksum]

Example - Power On:
AA 07 00 02 1C 3D E2
├─ AA: Magic byte
├─ 07: Command ID (Remocon IR)
├─ 00 02: Length = 2 bytes
├─ 1C 3D: Payload (Power)
└─ E2: Checksum
```

See `REMOTE_SOUND_CODES_REFERENCE.md` for complete payload mapping.

## 🎨 UI/UX Design

### Theme
- **Background**: Pure black (#000000)
- **Accent**: Bright blue (#0A84FF)
- **Alerts**: Red (#FF453A), Orange (#FF9F0A), Green (#30D158)
- **Text**: Off-white (#F5F5F7), Muted gray (#86868B)

### Interactions
- **Hover Effects**: Color transitions and border glows (150ms)
- **Click Animation**: Scale bounce (0.96x for 90ms)
- **Tab Transitions**: Smooth 200ms crossfade
- **Window Controls**: Hover scale (1.1x) with icon color change

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+I` | Toggle debug panel visibility |
| `Double-click Title Bar` | Toggle maximize/minimize |

## 🐛 Debugging

### Enable Debug Panel
1. Press `Ctrl+Shift+I` to show debug log
2. View all sent/received frames with timestamps
3. Use Frame Tester to manually test commands
4. Copy payload values and hex values for testing

### Debug Log Format
```
[HH:MM:SS.mmm] SEND  payload=[CH CODE] frame=[AA 07 00 02 ... Checksum]
[HH:MM:SS.mmm] RECV  [incoming hex bytes...]
```

## 📝 Configuration

### Config File Location
- **Path**: `%LOCALAPPDATA%\SC-AKX200\panasonic_config.json`
- **Contents**: Last used COM port and connection preferences
- **Auto-created** on first run

### Example Config
```json
{
  "last_port": "COM4"
}
```

## 🔒 Permissions & Security

- Application runs with **lowest privilege requirement** (no admin needed)
- Config stored in user AppData (protected from Program Files restrictions)
- No external network communication
- No telemetry or data collection
- All Bluetooth communication is local

## 🚀 Building the Installer

### Prerequisites
- Inno Setup 6.2+ (download from [jrsoftware.org](https://jrsoftware.org/isdl.php))
- All source files in project directory

### Build Steps
1. Open `SC-AKX200-Setup.iss` in Inno Setup
2. Click **Build** → **Compile**
3. Installer created in `Output/SC-AKX200-Setup.exe`
4. Distribute to users

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| flet | 0.86.5 | Desktop UI framework |
| pyserial | 3.5 | Bluetooth/Serial communication |
| Python | 3.14+ | Runtime environment |

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```powershell
# Install dev dependencies
pip install pyserial flet

# Run in development mode
python panasonic_akx200_control.py

# Test protocol frames
# Use debug panel (Ctrl+Shift+I) Frame Tester
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This project is developed independently and is not affiliated with Panasonic Corporation. SC-AKX200 is a trademark of Panasonic. Use at your own risk.

## 🙋 Support

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: See included markdown files for protocol details
- **Questions**: Use GitHub Discussions

## 📚 References

- **SPP Protocol**: Bluetooth Serial Port Profile specification
- **Flet**: Modern Python UI framework (https://flet.io)
- **PySerial**: Python serial port library (https://pyserial.readthedocs.io)

---

**Made with ❤️ for audio enthusiasts**

*Last Updated: August 14, 2026*
