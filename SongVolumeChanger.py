#
#parts of code stolen from:
#https://learnsharewithdp.wordpress.com/2022/10/13/normalize-the-volume-of-sound-clip-using-pydub/
#https://readthedocs.org/projects/audiosegment/downloads/pdf/latest/
#

from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import mediainfo
import os
from tkinter import filedialog
from time import sleep

class SongVolumeChanger(object):
    """The SongVolumeChanger object sets the volume of songs in a given folder to a given value.

It uses the pydub module for working on audio files. For files other than .wav, ffmpeg needs to be installed (mpeg.org).
(I used it for .mp3 files with ffmpeg, it worked ok.)
When instantiated, it immediately starts the process by calling the method to set the input folder."""
    def __init__(self):
        """Initializes the class.

It starts processing the songs by calling self.setInputFolder()."""
        self.formatList = ["wav", "mp3", ]
        os.system('cls')
        print("########################")
        print("Starting program...")
        self.setInputFolder()

    def setInputFolder(self):
        """Asks for the folder containing the songs.

It opens a tkinter dialogbox where you can set the input folder.
The input folder should only contain folders and audio files.
(Although processing skips files that throw an IndexError on opening with pydub.AudioSegment.from_file().)
Then starts the next step: set the target volume by calling self.setTargetVolume()."""
        answer = input("Set folder? (y/n) ")
        if answer.lower() == "y":
            self.inputFolderPath = filedialog.askdirectory()
        else:
            return
        if self.inputFolderPath == "":
            self.setInputFolder()
        else:
            self.setTargetVolume()

    def setTargetVolume(self):
        """Sets the target volume.

If the input string is not a number, self.targetVolume defaults to -10 (dB).
After that calls self.prepareOutput()."""
        os.system('cls')
        print("########################")
        print(f"Setting target volume...")
        inputString = input("Target volume? (dB) ")
        self.targetVolume = float(inputString) if inputString.isnumeric() else -10
        self.prepareOutput()

    def prepareOutput(self):
        """Creates an automatically named output folder if it doesn't exist.

The output folder's name is the input folder's name concatenated with _edited.
After that calls self.processing()."""
        os.system('cls')
        print("########################")
        print(f"Preparing output...")
        split = os.path.split(self.inputFolderPath)
        self.outputFolderName = split[1] + "_edited"
        self.outputFolderPath = "/".join([split[0], self.outputFolderName])
        if not os.path.exists(self.outputFolderPath):
            os.makedirs(self.outputFolderPath)
        self.processing()

    def processing(self):
        """Processes the songs the input folder.

It lists the files in the folder, then goes through the list.
For every song, it separates the format from the rest of the filename (based on the dot in 'name.format').
Then it tries to separate the name into artist and title (based on the hyphen in 'artist - title').
If only one hyphen is present, then it works ok, otherwise it sets artist as 'unknown' and title as the name.
A tag is created from this artist and title data.
Then opens the file and sets the volume using self.matchTargetVolume() and saves the modified song with the tag created above.
If the format is not audio, pydub.AudioSegment.from_file() should throw an IndexError and the file will be skipped.
The ouput filename is of the format 'artist - title', so for filenames with more than one hyphen it changes the original filename."""
        os.system('cls')
        print("########################")
        print(f"Processing...")
        inputSongs = os.listdir(self.inputFolderPath)
        inputSongs = [f for f in inputSongs if os.path.isfile(self.inputFolderPath+'/'+f)] #filtering only the files, should filter for audio files
        ##print(*inputFiles, sep="\n")
        N1 = len(inputSongs) #number of files (folder may contain other files than audio)
        N2 = 0 #number of actually processed audio files
        print(f"From: {self.inputFolderPath}")
        print(f"To: {self.outputFolderPath}")
        print(f"Target volume: {self.targetVolume}")
        sleep(2)
        for i in range(N1):
            os.system('cls')
            print("########################")
            print(f"Working on file {i+1}/{N1}...")
            songName = inputSongs[i]
            split1 = songName.split(".") #to get format at the end
            songFormat = split1[-1]
            
##            if songFormat not in self.formatList:
##                print("Error: possibly wrong format. Moving to next file.")
##                continue
            
##            map(str.strip, songName.split("-")) #???
            withoutFormat = ".".join(split1[0:len(split1)-1])
            split2 = withoutFormat.split("-") #to separate artist and title, if possible
            if len(split2) == 2:
                artist, title = split2
                artist = artist.strip()
                title = title.strip()
            else:
                artist, title = "unknown", songName
            print(f"{artist} - {title}")
            tags = {"artist": artist, "title" : title} #create tags metadata
##            originalTags = mediainfo(songName)#.get('TAG', {})
##            print(originalTags)
            songPath = os.path.abspath(os.path.join(self.inputFolderPath, songName))
            try:
                sound = AudioSegment.from_file(songPath, format=songFormat)
            except IndexError:
                print("Error: possibly wrong format. Moving to next file.")
                continue
            N2 += 1
##            print(sound.dBFS)
##            play(sound)
            modifiedSound = self.matchTargetVolume(sound, self.targetVolume) #set the volume
            outputName = artist + " - " + title + "." + songFormat
            outputPath = self.outputFolderPath + "\\" + outputName
            modifiedSound.export(outputPath, format=songFormat, tags=tags)
        os.system('CLS')
        print("########################")
        print("Complete")
        print(f"{N2} song(s) processed in {self.inputFolderPath}")

    def matchTargetVolume(self, sound, targetVolume):
        """Sets the volume of sound to targetVolume."""
        deltaVolume = targetVolume - sound.dBFS
        return sound.apply_gain(deltaVolume)

if __name__ == "__main__":
    SVC = SongVolumeChanger()
