@ECHO OFF

IF "%1"=="install" GOTO install
IF "%1"=="run" GOTO run
IF "%1"=="clean" GOTO clean
GOTO :EOF

:install
	echo Installing dependencies...
	python -m pip install -r requirements.txt
	GOTO :EOF

:run
	echo Running Django Server...
	python manage.py runserver
	GOTO :EOF

:clean
	echo Cleaning up...
	rd /s /q __pycache__
	GOTO :EOF
