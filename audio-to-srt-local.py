import os
import subprocess
import argparse

from vosk import Model, KaldiRecognizer, SetLogLevel

SAMPLE_RATE = 16000

# SetLogLevel(-1)

parser = argparse.ArgumentParser(usage="%(prog)s <FILE>", description="generate a srt from a video.")
parser.add_argument('files', nargs="*")
parser.add_argument('-f', help='force overwrite', action='store_true')
parser.add_argument('-m', help='model path', default='vosk-model-en-us-0.22')
parser.add_argument('-v', help='verbose output', action='store_true')
args = parser.parse_args()

model = Model(args.m)
rec = KaldiRecognizer(model, SAMPLE_RATE)
rec.SetWords(True)

for f in args.files:
    with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                          f,
                          "-ar", str(SAMPLE_RATE), "-ac", "1", "-f", "s16le", "-"],
                          stdout=subprocess.PIPE).stdout as stream:

        res = rec.SrtResult(stream)
        if args.v:
            print(res)
        path, file = os.path.split(f)
        fname, _ = os.path.splitext(file)
        # print(f"file: {file} path: {path}")
        outfile = f"{path}{os.sep if path else ''}{fname}-recognized.srt"
        print(outfile)
        if args.f or not os.path.isfile(outfile):
            with open(outfile, "w") as text_file:
                text_file.write(res)
        else:
            print(f"{outfile} exists, skipping")
