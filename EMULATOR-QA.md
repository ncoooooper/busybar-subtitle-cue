# Emulator verification

Actual SRT parser, playback clock and a three-cue rehearsal script.

Sought to the second cue, started and paused playback, stepped back, then returned to the second cue at 00:05.

17 distinct frames were recorded on firmware 1.3.1. App io.ncoooooper.subtitlecue exited: finished; heap peak 79.3 of 128 KiB. Screenshots are in screenshots/ and the recording is in media/.

## Display capture

Firmware 1.3.1 rendered both README examples. The display run replayed sample inputs in a separate emulator project. The source test above describes how those readings were obtained. Each square in a guide GIF is one front-display pixel enlarged to 9 × 9. The production archive was built from the source in this repository.
