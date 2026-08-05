@echo off
cd /d "C:\MediVoice"
echo Starting MediVoice App...
start "" /MIN cmd /c "cd /d C:\MediVoice && set \"SMTP_HOST=smtp.gmail.com\" && set \"SMTP_PORT=587\" && set \"SMTP_USER=n7141072@gmail.com\" && set \"SMTP_PASSWORD=icswxictwfvjslof\" && set \"SMTP_SENDER=n7141072@gmail.com\" && set \"SMTP_USE_TLS=true\" && streamlit run demo.py --server.headless true --server.port 8529"
timeout /t 5 >nul
start "" msedge --app="http://localhost:8529"
exit
