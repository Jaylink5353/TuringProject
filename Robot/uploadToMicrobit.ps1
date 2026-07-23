
& "C:\Users\Jaymes\PycharmProjects\TuringProject\.venv\Scripts\activate.ps1"


Copy-Item microbitMain.py main.py
ufs put main.py
Remove-Item main.py
ufs put .\piSerialLibmk3.py
ufs put .\keyes_mecanum_car_v2.py
ufs ls
deactivate