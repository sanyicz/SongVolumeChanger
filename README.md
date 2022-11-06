# SongVolumeChanger
I created this program because I needed to set the volume of a number of songs to the same value.

It uses the pydub module for working on audio files. For files other than .wav, ffmpeg needs to be installed (mpeg.org).
I used it for .mp3 files with ffmpeg, it worked ok.

It lists the files in the given folder, then goes through the list.
For every song, it separates the format from the rest of the filename (based on the dot in 'name.format').
Then it tries to separate the name into artist and title (based on the hyphen in 'artist - title').
If only one hyphen is present, then it works ok, otherwise it sets artist as 'unknown' and title as the name.
A tag is created from this artist and title data.
Then opens the file, sets the volume and saves the modified song with the tag created above.
If the format is not audio, pydub.AudioSegment.from_file() should throw an IndexError and the file will be skipped.
The ouput filename is of the format 'artist - title', so for filenames with more than one hyphen it changes the original filename.
