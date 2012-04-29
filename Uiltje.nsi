; We use NSIS
;   http://nsis.sourceforge.net/
; and its Self-Extractor Kit
;   http://nsis.sourceforge.net/NSIS_Self-Extractor_kit

!include "SE.nsh"

${SE-HeadingLine1} 		"Uiltje"
${SE-HeadingLine2} 		"versie 1"
${SE-Product}			"Uiltje versie 1"

${SE-OutFile}			"Uiltje.exe"
${SE-ExtractDir}		"$PROGRAMFILES\Uiltje"
${SE-AutoClose}
${SE-ExtractList}       show
${SE-ExecOnClose}
${SE-ExecCheckBox}      "$INSTDIR\main.exe" "Start Uiltje na installatie"

;- Files to extract
${SE-FilesStart}

 ${SE-OutPath} "$INSTDIR"
  ${SE-AddDir} "dist\main" r

${SE-FilesEnd}

${SE-ShortcutsStart}
 ${SE-OutPath} "$SMPROGRAMS"
  ${SE-Shortcut} "$SMPROGRAMS\Uiltje.lnk" "$INSTDIR\main.exe"
${SE-ShortcutsEnd}