@echo off 
echo Downloading icon... 
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/iconic/open-iconic/master/png/check-4x.png', 'temp_icon.png')" 
echo If icon download fails, please manually save an icon as 'icon.ico' in this folder. 
pause 
