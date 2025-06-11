; installer/setup.iss
#define MyAppName "Tower Defense"
#define MyAppVersion "1.0.0"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={pf}\{#MyAppName}
OutputBaseFilename={#MyAppName}Setup{#MyAppVersion}
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico

[Files]
Source: "..\dist\tower_defense.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\tower_defense.exe"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\tower_defense.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"