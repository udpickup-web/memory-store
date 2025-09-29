# BOT — Внешняя зашифрованная память (каркас)
Целевой путь установки: **C:\PROG\BOT**

## Быстрый старт (Windows CMD)
```cmd
cd /d C:\PROG\BOT
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

REM сгенерируй ключ и создай .env
.venv\Scripts\python tools\keygen.py > tmp_key.txt
type tmp_key.txt
copy /y .env.example .env
notepad .env

REM тест шифрования/дешифрования
echo test>sample.txt
.venv\Scripts\python tools\encrypt.py sample.txt encrypted\memory\sample.txt.enc --aad manifest:1.0
.venv\Scripts\python tools\decrypt.py encrypted\memory\sample.txt.enc out_sample.txt --aad manifest:1.0
type out_sample.txt

REM обнови manifest и при желании запушь
.venv\Scripts\python tools\checksum.py update-manifest
.venv\Scripts\python tools\push_git.py
```
