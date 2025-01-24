# How to generate voiceover and subtitles for a (Powerpoint) presentation

Assuming you want good audio quality and want to avoid using YouTube for the generation of subtitles for some reason (time e.g.).

## Guide for those in a hurry

1. Make a presentation. Avoid:
   1. Animations, make incremental slides for that
   2. If really necessary, you should extract the animated slides to a separate presentation later and render that out as a video.
1. Type the Audio track in the slide notes. You can check overall length by running notes-to-wav.ps1 and loading the audio into your favorite music player, like [foobar2000](https://www.foobar2000.org/)
1. Export all slides as PNGs
1. Use some service to generate high-quality speech from the `allnotes.txt`, like [Play.ht](Play.ht)
1. Use your favorite video editor to arrange the slides according to the audio track, fine tune etc.
1. Render the video
1. You can use the vosk [transcriber](https://alphacephei.com/vosk/install) or, to make sure a local model is used
   1. `pip install vosk`
   1. have ffmpeg installed and in the path
   1. download the model from https://alphacephei.com/vosk/models
   1. use `audio-to-srt-local.py -m <modelpath> <video.mp4>`, this will write `video-recognized.srt`
   1. clean up/merge the subtitles using https://aegisub.org/downloads/
1. Import the srt into the video editor
1. Further adjust subtitles and timing
1. Re-Export subtitles
1. Profit.


## Requirements
`pip install python-dotenv vosk pyht`


## The scripts

### notes-to-wav.ps1
This script generates several things for you:
* `Slide[\n+].txt` containing the notes text separated by slide
* `Slide[\n+].wav` containing the text synthesized by System.Speech.Synthesis.SpeechSynthesizer - this is helpful to keep track of the total talking time mostly
* `allnotes.txt` the whole text in a single file

## audio-to-srt.py (deprecated)
This script generates a `.srt` from an audio track using the strategy described [here](https://picovoice.ai/blog/how-to-create-subtitles-for-any-video-with-python/)

## audio-to-srt-local.py
Generates a `.srt` directly from a video file using ffmpeg and vosk and a local model (download the model manually).
