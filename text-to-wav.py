import glob
import os
import argparse
from dotenv import dotenv_values
from pyht import Client
from pyht.client import TTSOptions

parser = argparse.ArgumentParser(usage="%(prog)s <FILE>", description="transform text to wav via play.ht")
parser.add_argument('files', nargs="*")
parser.add_argument('-f', help='force overwrite', action='store_true')
parser.add_argument('-v', help='verbose output', action='store_true')
args = parser.parse_args()

secrets = dotenv_values(".secrets")

if "PLAY_HT_USER_ID" not in secrets.keys() and "PLAY_HT_API_KEY" not in secrets.keys():
    print("Please provide PLAY_HT_USER_ID and PLAY_HT_API_KEY in .secrets")
    exit(1)

# client = Client(
#     user_id=secrets["PLAY_HT_USER_ID"],
#     api_key=secrets["PLAY_HT_API_KEY"]
# )

# options = TTSOptions(format="wav", sample_rate=48000, voice="TODO")  # TODO voice

for f in args.files:
    input = glob.glob(f)
    for i in input:
        path, file = os.path.split(i)
        fname, _ = os.path.splitext(file)
        outfile = f"{path}{os.sep if path else ''}{fname}.wav"
        print(f"{i} -> {outfile}")

        text = open(i).read()
        # no output yet
        print(text)
        # if args.f or not os.path.isfile(outfile):
        #     with open(outfile, "wb") as audio_file:
        #         for chunk in client.tts(text, options, voice_engine = 'PlayDialog-http'):
        #             audio_file.write(chunk)
        # else:
        #     print(f"{outfile} exists, skipping")
