@echo off
SETLOCAL

set RUNTIME_HOST=0.0.0.0
set RUNTIME_PORT=8001
set ENVIRONMENT=production

uvicorn main:app --port %RUNTIME_PORT% --host %RUNTIME_HOST% --proxy-headers --ssl-keyfile ./certificate/privatekey.pem --ssl-certfile ./certificate/certificate.pem

ENDLOCAL
