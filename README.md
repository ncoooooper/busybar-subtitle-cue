# Subtitle Cue

Rehearse a timed SRT script, pause on a line and seek directly between subtitle cues.

Hold a difficult line in view during rehearsal and restart from its timestamp. You can loop the troublesome part of a script while leaving the source subtitles intact.

## Seek to the line you need

1. Start the local reader with your timed SRT script. Check the cue number and timestamp on the front and the words on the rear.
2. Turn the wheel to step to another cue. Click to begin or resume time-based playback from the selected location.
3. Click again to pause on a line. The clip moves from the first cue at 00:01 to the second at 00:05.

![Cue 1/3 at 00:01 gives way to playback at cue 2/3 at 00:05.](media/guide/seek-and-start.gif)

## Rehearse the same exchange

1. While paused, turn back one cue for the lead-in and forward again to repeat the line. The clip shows both jumps.
2. Hold the wheel to page through a cue too long for the rear display. Hold **Start** when you want to rewind the script.
3. Cue timing comes from the SRT. Change a timing in the subtitle file itself if the performance calls for a different duration.

![The paused display jumps back to cue one and forward to cue two again.](media/guide/revisit-paused-cue.gif)

## Example from the emulator

The test script has three cues. Seeking to the second lands exactly at 00:05. The front is a timing reference for the speaker while the rear carries the actual rehearsal text. The companion parsed a local three-cue SRT file and ran the rehearsal clock.

## Set up the source

Run python3 companion/serve.py /path/to/script.srt. Set bridge to http://127.0.0.1:8770/reading in the emulator. Wheel seeks through the full script, click pauses or resumes and holding the wheel pages long cues. Hold Start rewinds. Timing follows the source SRT file. The rear display uses the fonts available in the firmware. For hardware, use --bind with your computer's LAN address on a trusted local network and use that address in the URL.

## Run in the emulator

Open BUSY Bar Emulator. From this repository, run:

```sh
~/.busy-emulator/bin/busy-emulator dev --once
```

Press **Back** to exit.

The GIFs are excerpts from the emulator recording. Each front-display pixel is shown at 9× its original width and height. The end frames pause for reading.

[Full recording](media/controls.mp4) · [Rear display](screenshots/back-1.png) · [Firmware test](EMULATOR-QA.md) · [MIT license](LICENSE)
