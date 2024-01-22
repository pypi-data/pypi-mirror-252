from main import Downloader
import time

link = "https://objects.githubusercontent.com/github-production-release-asset-2e65be/461109158/3ca53660-8917-4fc1-bb0f-0caeb36fbe5c?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20240121%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240121T103241Z&X-Amz-Expires=300&X-Amz-Signature=ed0cdce60b91135d965a8525f58d5bc9b5a4afb15198207343e1ce01744a4b74&X-Amz-SignedHeaders=host&actor_id=83004520&key_id=0&repo_id=461109158&response-content-disposition=attachment%3B%20filename%3Dalt.app.installer.exe&response-content-type=application%2Foctet-stream"
dl = Downloader()
dl.start(link, "test\\", display=True, multithread=True, segments=2, block=False)
time.sleep(2)
dl.stop()
dl.start(link, "test\\", display=True)
# dl.start(link, "test\\", display=True, multithread=False)
