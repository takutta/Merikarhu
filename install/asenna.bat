cmd /c powershell -Nop -NonI -Nologo -WindowStyle Hidden "Write-Host"
@echo off
python -m venv %USERPROFILE%\Desktop\skripti
copy skripti.py %USERPROFILE%\Desktop\skripti
copy requirements.txt %USERPROFILE%\Desktop\skripti
copy icon.ico %USERPROFILE%\Desktop\skripti
powershell.exe -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Desktop\aloita.lnk'); $s.TargetPath='C:\Python311\python.exe'; $s.Arguments='%userprofile%\Desktop\skripti\skripti.py'; $s.IconLocation='%userprofile%\Desktop\skripti\icon.ico'; $s.Save()"
cmd /k "cd /d %USERPROFILE%\Desktop\skripti\Scripts && activate && cd .. && pip install -r requirements.txt && python skripti.py && exit"
