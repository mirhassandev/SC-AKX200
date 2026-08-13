; Inno Setup Script for SC-AKX200 Control Panel
; Professional installer with comprehensive icon support

[Setup]
AppName=SC-AKX200 Control Panel
AppVersion=1.0.0
AppPublisher=Panasonic
AppPublisherURL=https://github.com
AppSupportURL=https://github.com
AppUpdatesURL=https://github.com
AppId={{A9B4D5E3-1234-5678-9ABC-DEF012345678}}
DefaultDirName={pf}\SC-AKX200 Control Panel
DefaultGroupName=SC-AKX200
AllowNoIcons=no
LicenseFile=
OutputDir=.\Output
OutputBaseFilename=SC-AKX200-Setup
SetupIconFile=Guillendesign-Variations-3-Music.ico
WizardSmallImageFile=wizard.bmp
UninstallDisplayIcon={app}\Guillendesign-Variations-3-Music.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
WizardStyle=modern
WizardResizable=yes
ChangesAssociations=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Types]
Name: "full"; Description: "Full installation"
Name: "compact"; Description: "Compact installation"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "app"; Description: "SC-AKX200 Control Panel"; Types: full compact custom; Flags: fixed
Name: "python"; Description: "Python 3.14+ Runtime"; Types: full; Flags: fixed
Name: "docs"; Description: "Documentation"; Types: full custom

[Files]
Source: "panasonic_akx200_control.py"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "SC-AKX200.bat"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "SC-AKX200.vbs"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "install_deps.py"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "Guillendesign-Variations-3-Music.ico"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "wizard.bmp"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "PROTOCOL_FIX_SUMMARY.md"; DestDir: "{app}"; Components: docs; Flags: ignoreversion
Source: "REMOTE_SOUND_CODES_REFERENCE.md"; DestDir: "{app}"; Components: docs; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Components: app; Flags: ignoreversion

[Icons]
Name: "{group}\SC-AKX200 Control Panel"; Filename: "wscript.exe"; Parameters: """{app}\SC-AKX200.vbs"""; IconFilename: "{app}\Guillendesign-Variations-3-Music.ico"; IconIndex: 0; Comment: "Panasonic SC-AKX200 Control Panel"; WorkingDir: "{app}"
Name: "{commondesktop}\SC-AKX200"; Filename: "wscript.exe"; Parameters: """{app}\SC-AKX200.vbs"""; IconFilename: "{app}\Guillendesign-Variations-3-Music.ico"; IconIndex: 0; Comment: "Panasonic SC-AKX200 Control Panel"; WorkingDir: "{app}"
Name: "{group}\{cm:UninstallProgram,SC-AKX200}"; Filename: "{uninstallexe}"; IconFilename: "{app}\Guillendesign-Variations-3-Music.ico"

[Run]
Filename: "wscript.exe"; Parameters: """{app}\SC-AKX200.vbs"""; WorkingDir: "{app}"; Description: "Launch SC-AKX200 Control Panel"; Flags: postinstall skipifsilent

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{{A9B4D5E3-1234-5678-9ABC-DEF012345678}}"; ValueType: string; ValueName: "DisplayIcon"; ValueData: "{app}\Guillendesign-Variations-3-Music.ico"; Flags: uninsdeletekey

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
