; We use NSIS
;   http://nsis.sourceforge.net/

!define version "beta 3"

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\Uiltje"
OutFile "Uiltje ${version}.exe"
Icon "uiltje.ico"
AutoCloseWindow true
ShowInstDetails show
ShowUninstDetails show

Section
	SetOutPath $INSTDIR
	File /r /x dist\main\var dist\main\*
	WriteUninstaller $INSTDIR\uninstaller.exe
	CreateShortCut "$DESKTOP\Uiltje.lnk" "$INSTDIR\uiltje.exe"
	CreateDirectory "$SMPROGRAMS\Uiltje"
	CreateShortCut "$SMPROGRAMS\Uiltje\Uiltje.lnk" \
							"$INSTDIR\uiltje.exe"
	CreateShortCut "$SMPROGRAMS\Uiltje\Verwijder Uiltje.lnk" \
							"$INSTDIR\uninstaller.exe"
SectionEnd

Section "Uninstall"
	RMDir /r $INSTDIR
	RMDir /r "$SMPROGRAMS\Uiltje"
	Delete $DESKTOP\Uiltje.lnk
SectionEnd

Function .onInstSuccess
	Exec $INSTDIR\uiltje.exe
FunctionEnd