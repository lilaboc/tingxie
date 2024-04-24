import asyncio
import importlib.resources
import random
import re
import sys
import tempfile
import time

import aioconsole
import edge_tts
from playsound import playsound


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main())


def phonics():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_phonics())


async def _phonics():
    if len(sys.argv) == 2:
        words = [
            i.strip()
            for i in importlib.resources.open_text(
                "tingxie", "words_alpha.txt"
            ).readlines()
            if len(i.strip()) <= int(sys.argv[1])
        ]
    else:
        words = [
            i.strip()
            for i in importlib.resources.open_text(
                "tingxie", "words_alpha.txt"
            ).readlines()
        ]
    while True:
        word = random.choice(words)
        print(word)
        media = (
            await asyncio.gather(aioconsole.ainput(">>>"), edge(word, slow=False))
        )[1]
        playsound(media)


async def _main():
    # engine = pyttsx3.init()
    if len(sys.argv) == 1:
        print("tingxie file.txt")
        while True:
            media = await edge(input(">>>").strip(), slow=False)
            playsound(media)
    else:
        start = time.time()
        for filename in sys.argv[1:]:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if line.strip() != "":
                        while True:
                            media = await edge(line.strip(), slow=False)
                            playsound(media)
                            print(random.randint(0, 10))
                            i = await aioconsole.ainput(">>>")
                            if i.strip() != "r":
                                break
                            else:
                                continue

        print(time.strftime("%H:%M:%S", time.gmtime(time.time() - start)))


async def edge(text, slow=True):
    if slow:
        result = edge_tts.Communicate(text, get_voice(text), rate="-50%")
    else:
        result = edge_tts.Communicate(text, get_voice(text))
    media = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    media.close()
    await result.save(media.name)
    return media.name


def get_voice(text):
    chinese = [
        "zh-CN-XiaoxiaoNeural",
        "zh-CN-XiaoyiNeural",
        "zh-CN-YunjianNeural",
        "zh-CN-YunxiNeural",
        "zh-CN-YunxiaNeural",
        "zh-CN-YunyangNeural",
    ]
    english = [
        "en-US-AnaNeural",
        "en-US-AriaNeural",
        "en-US-ChristopherNeural",
        "en-US-EricNeural",
        "en-US-GuyNeural",
        "en-US-JennyNeural",
        "en-US-MichelleNeural",
        "en-US-RogerNeural",
        "en-US-SteffanNeural",
        "en-GB-LibbyNeural",
        "en-GB-MaisieNeural",
        "en-GB-RyanNeural",
        "en-GB-SoniaNeural",
        "en-GB-ThomasNeural",
    ]
    if re.search("[\u4e00-\u9fff]", text):
        # return "zh-CN-YunxiNeural"
        return random.choice(chinese)
    # return "en-US-ChristopherNeural"
    return random.choice(english)


if __name__ == "__main__":
    main()
    # phonics()
