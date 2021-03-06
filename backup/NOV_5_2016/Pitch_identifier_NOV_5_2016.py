# program Pitch_identifier_NOV_1_2016
# programmer Oliver Zhang
# date Nov 1 2016

import pygame
from pygame import *
import pyaudio
import struct
import sys
import wave
import signalprocessing as sp

pygame.init()
width, height, = 800, 600
back_color = (240, 240, 240)
clock = pygame.time.Clock()
screen = display.set_mode((width, height), RESIZABLE)
display.set_caption("Oliver Zhang Pitch Identifier")

AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

using_sharps = True
SHARP_CHAR = u'\u266F'
FLAT_CHAR = u'\u266D'
TEXT_COLOR = (70, 70, 70)


identified_freq = None

def record_chunk():
    stream.start_stream()
    for i in range(2):
        audio_data = stream.read(CHUNK)
        if i == 1:
            samples = struct.unpack(str(CHUNK) + "h", audio_data)
    stream.stop_stream()
    return samples

def write_to_file(filename, samples):
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(AUDIO_FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(struct.pack(str(CHUNK) + "h", *samples))
    waveFile.close()


def events():
    global done, width, height, identified_freq, current_samples
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == VIDEORESIZE:
            width, height = event.size
            screen = display.set_mode((width, height), RESIZABLE)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
            if event.key == K_SPACE:
                samples = record_chunk()
                # write_to_file("output/output" + str(frame) + ".wav", samples)
                identified_freq = sp.identify_freq(samples=sp.normalize(samples), samprate=RATE,
                                                   start_freq=sp.note_to_hertz("A", accidental=None, octave=2),
                                                   end_freq=sp.note_to_hertz("A", accidental=None, octave=6),
                                                   step_semitones=1, thres_cents=1)


def render():
    screen.fill(back_color)
    if identified_freq == None:
        # render instruction text
        f = pygame.font.SysFont("segoe ui", 24)
        note_text = f.render("Press space to identify pitch", True, TEXT_COLOR)
        note_x = width / 2 - note_text.get_rect().centerx
        note_y = height / 2 - note_text.get_rect().height
        screen.blit(note_text, Rect(note_x, note_y, 0, 0))
        display.update()
        return
    letter_name, octave, cents = sp.hertz_to_note(identified_freq)

    # tuple of enharmonically equivalent note names.
    if type(letter_name) == tuple:
        if using_sharps:
            letter_name = letter_name[0]
        else:
            letter_name = letter_name[1]
        letter_name = letter_name.replace("#", SHARP_CHAR)
        letter_name = letter_name.replace("b", FLAT_CHAR)
    if cents > 0:
        cents = ", +" + str(cents) + " cents"
    elif cents < 0:
        cents = ", " + str(cents) + " cents"
    else:
        cents = ""

    # render note name text
    f = pygame.font.SysFont("segoe ui", 96)
    note_text = f.render(letter_name + unichr(8320 + octave), True, TEXT_COLOR)
    note_x = width/2 - note_text.get_rect().centerx
    note_y = height/2 - note_text.get_rect().height
    screen.blit(note_text, Rect(note_x, note_y, 0, 0))

    # render pitch information text
    f = pygame.font.SysFont("segoe ui", 24)
    freq_text = f.render(str(round(identified_freq, 2)) + "Hz" + cents, True, TEXT_COLOR)
    freq_x = width/2 - freq_text.get_rect().centerx
    freq_y = height/2
    screen.blit(freq_text, Rect(freq_x, freq_y, 0, 0))
    display.update()


# begin recording
audio = pyaudio.PyAudio()
stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)


# Wait out the latency period
done_latency = False
while not done_latency:
    samples = struct.unpack(str(CHUNK) + "h", stream.read(CHUNK))
    for sample in samples:
        if sample < -1 or sample > 1:
            done_latency = True
            break
stream.stop_stream()


done = False
frame = 0
while not done:
    clock.tick(10)
    events()
    render()
    frame += 1
pygame.quit()
sys.exit()