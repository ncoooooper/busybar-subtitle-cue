# Subtitle Cue

Rehearse a timed SRT script, pause on a line and seek directly between subtitle cues.

Run python3 companion/serve.py /path/to/script.srt. Set bridge to http://127.0.0.1:8770/reading in the emulator. Wheel seeks through the full script, click pauses or resumes and holding the wheel pages long cues. Hold Start rewinds. Timing follows the source SRT file. The rear display uses the fonts available in the firmware. For hardware, use --bind with your computer's LAN address on a trusted local network and use that address in the URL.

## Run locally

From this folder, run `~/.busy-emulator/bin/busy-emulator dev --once` with BUSY Bar Emulator open. Back exits.

![BUSY Bar front display](screenshots/front-1.png)
