# transcriber

Transcriber is able to take in microphone input and output a very crude sheet music approximation to the detected frequencies. This program is still very much in it's infancy and is unable to detect rhythms or perform overtone removal.

At the heart of this program is the discrete fourier transform (DFT). Its job is to transform microphone audio in the time domain (not useful for our purposes) into the frequency domain. Array processing from Numpy is used to make this happen efficiently. 

Pygame is used to render the results of the spectrogram on the screen with a black-red-yellow-white colormap.

For most accurate note detection, there are thresholds for the both minimum value and the time-derivative of frequency intensities that need to be calibrated (slightly) depending on the nature of the sound source. Having a threshold for time-derivative of frequency intensities ensures that one continuous tone is not detected as multiple notes being played in rapid succession.

Once the notes have been detected, the mingus library formats the detected notes into a file compatible with lilypond, which is an external application that does the sheet music engraving to pdf format.

#### Dependencies:
* Python 2.7.9
* PyAudio 0.2.9
* numpy 1.11.2
* pygame 1.9.2a0
* lilypond 2.16.0
* mingus 0.5.1
