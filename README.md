# siasnip
A snipping tool that uploads directly to Sia Skynet.
### Dependecies
- pyperclip
- configparser
- siaskynet
- playsound
- PyQt5
- Pillow
- desktopmagic

install dependencies using:
`pip install [dependency name]`

### Usage
Running siasnip.py will start the snipping tool, dragging a rectangle will then capture that part of the screen and upload it to Sia Skynet.

If desired, siasnip.py can be renamed to siasnip.pyw (to run without a terminal) and can be opened however the user desires (e.g Autohotkey/batch script).

### Demo Video

https://siasky.net/AACFzFXVy9_AwtH-bqBB4g6sBHuMbh8TK42VBdYSxLvT5g

### Config
Config information is saved in the cfg.ini, each affects the function of siasnip: 
- uploadportaladdress: portal address that will be used to upload the screengrab to skynet
- linkportaladdress: portal address that is appended to the start of the skylink when added to the clipboard
- beepfilename: filename for the .mp3/.wav that is played when the file is uploaded