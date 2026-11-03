; Inno Setup script. Build from the repo root, after PyInstaller:
;   iscc /DAppVersion=1.0.0 packaging\windows\installer.iss

#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif

[Setup]
AppId={{B6D1A0E2-5C0F-4B7A-9E38-4F2D1C7A9A11}
AppName=FinanceTracker
AppVersion={#AppVersion}
AppPublisher=Leonardo de Almeida
DefaultDirName={autopf}\FinanceTracker
DefaultGroupName=FinanceTracker
DisableProgramGroupPage=yes
OutputDir=..\..\dist
OutputBaseFilename=FinanceTracker-{#AppVersion}-windows-setup
SetupIconFile=..\..\assets\icon.ico
UninstallDisplayIcon={app}\FinanceTracker.exe
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "..\..\dist\FinanceTracker\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\FinanceTracker"; Filename: "{app}\FinanceTracker.exe"
Name: "{autodesktop}\FinanceTracker"; Filename: "{app}\FinanceTracker.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\FinanceTracker.exe"; Description: "{cm:LaunchProgram,FinanceTracker}"; Flags: nowait postinstall skipifsilent
