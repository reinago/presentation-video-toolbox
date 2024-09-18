# How to generate voiceover and subtitles for a (Powerpoint) presentation

Assuming you want good audio quality and want to avoid using YouTube for the generation of subtitles for some reason (time e.g.).

## Guide for those in a hurry

1. Make a presentation. Avoid:
   1. Animations, make incremental slides for that
   2. If really necessary, you should extract the animated slides to a separate presentation later and render that out as a video.
2. Type the Audio track in the slide notes. You can check overall length by running notes-to-wav.ps1 and loading the audio into your favorite music player, like [foobar2000](https://www.foobar2000.org/)
3. Export all slides as PNGs
4. Use some service to generate high-quality speech from the `allnotes.txt`, like [Play.ht](Play.ht)
5. Use your favorite video editor to arrange the slides according to the audio track, fine tune etc.
6. Render the video
7. Extract the final audio track, e.g. using `ffmpeg -i <video> -vn output-audio.wav`
8. Feed it back into [picovoice](https://console.picovoice.ai/) using `audio-to-srt.py`
9. Import the srt into the video editor
10. Fix subtitles and timing
11. Re-Export subtitles
12. Profit.





## The scripts

### notes-to-wav.ps1
This script generates several things for you:
* `Slide[\n+].txt` containing the notes text separated by slide
* `Slide[\n+].wav` containing the text synthesized by System.Speech.Synthesis.SpeechSynthesizer - this is helpful to keep track of the total talking time mostly
* `allnotes.txt` the whole text in a single file

## audio-to-srt.py
This script generates a `.srt` from an audio track using the strategy described [here](https://picovoice.ai/blog/how-to-create-subtitles-for-any-video-with-python/)
