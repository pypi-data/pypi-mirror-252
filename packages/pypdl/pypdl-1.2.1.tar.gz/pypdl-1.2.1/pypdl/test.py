from pypdl import Downloader

link = "https://gamedownloads.rockstargames.com/public/installer/Rockstar-Games-Launcher.exe"
dl = Downloader()
# dl.start(link, "test\\", display=True, multithread=True, segments=2, block=False)
# time.sleep(2)
# dl.stop()
dl.start(link, "test")
# dl.start(link, "test\\", display=True, multithread=False)
