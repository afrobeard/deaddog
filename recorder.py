import pyaudio
import wave
import os
import urllib2
import urllib
import base64
import json

WAVE_OUTPUT_FILENAME = "file.wav"
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 7


def record_sound_clip():
    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print "Starting Recording Please Speak for 15 seconds"
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print "Finished Recording"


    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def convert_audio_to_text():
    username = "9c811611-e318-401e-ad85-964540af0909"
    password = "mmuTs53xXOvV"
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    data = open(WAVE_OUTPUT_FILENAME).read()
    req = urllib2.Request('https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?' + \
                          'timestamps=true&word_alternatives_threshold=0.9', data)
    req.add_header('Content-Length', '%d' % len(data))
    req.add_header('Content-Type', 'audio/wav')
    req.add_header("Authorization", "Basic %s" % base64string)

    res = urllib2.urlopen(req)
    str_resp = res.read()
    d = json.loads(str_resp)
    txt_response = d["results"][0]['alternatives'][0]
    return txt_response

def recommendations(input_string):
    username = "f7b80c7f-f38c-48ba-b9aa-df084b18aad3"
    password = "wDMumbSiYyND"
    prefix = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/341781x90-nlc-511/classify?"
    params = urllib.urlencode({
        "text": input_string
    }, True)
    data_url = prefix + params
    req = urllib2.Request(data_url)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    req = urllib2.Request(data_url)
    req.add_header("Authorization", "Basic %s" % base64string)
    res = urllib2.urlopen(req)
    str_resp = res.read()
    d = json.loads(str_resp)
    return d["classes"][0]


def loop():
    if True:
        while True:
            continue_txt = input('Type "Start" to start recording: ')
            if 'start' in continue_txt.lower():
                pass
            else:
                exit(0)
            record_sound_clip()
            resp = convert_audio_to_text()
            print repr(resp)
            print "Confidence %s Transcript %s"%(resp.get('confidence'), resp.get('transcript'))
            resp = recommendations(resp.get('transcript'))
            print repr(resp)
            print "Triaging issue into %s class. Confidence %s"%(resp.get('class_name'), float(resp.get('confidence')) * 100)
            continue_txt = input('Type "Continue" to go again: ')
            if 'continue' in continue_txt.lower():
                continue

loop()
