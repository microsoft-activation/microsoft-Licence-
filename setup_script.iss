[Setup]
AppName=Windows Activator Tool
AppVersion=1.0
DefaultDirName={commonpf}\WindowsActivatorTool
DefaultGroupName=Windows Activator Tool
OutputDir=Output
OutputBaseFilename=WindowsActivatorSetup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
UninstallDisplayIcon={app}\icon.ico

[Files]
Source: "dist\main_gui.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "win8_10_11.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "win7_later.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "alt_method.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Windows Activator Tool"; Filename: "{app}\main_gui.exe"; IconFilename: "{app}\icon.ico"
Name: "{commondesktop}\Windows Activator Tool"; Filename: "{app}\main_gui.exe"; IconFilename: "{app}\icon.ico"

[Run]
Filename: "{app}\main_gui.exe"; Description: "Launch Windows Activator Tool"; Flags: postinstall nowait skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"