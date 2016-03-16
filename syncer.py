import os
from pydub import AudioSegment
import subprocess

if os.name == "nt":
	FFMPEG_BIN = r"C:\\ffmpeg\\bin\\ffmpeg.exe"
	AudioSegment.converter = FFMPEG_BIN
else:
	FFMPEG_BIN = "ffmpeg"

print("Syncer 1.0")
crop_value = input("Please specify crop value 0-159. 0 - without cropping: ")

while int(crop_value) not in range(0, 160):
	try:
		print("You should type value between 0 and 159.")
		crop_value = int(input("Please specify crop value 0-159. 0 - without cropping: "))
	except ValueError:
		pass


if not os.path.exists("Result"):
	os.makedirs("Result")


output = AudioSegment.empty()

for wave in os.listdir("Audio"):
	if wave.endswith(".wav"):
		sound = AudioSegment.from_file("Audio/{}".format(wave))[int(crop_value):160]
		output = output.append(sound, crossfade=0)

audio_name = "Result/AudioCrop" + "_" + crop_value + ".wav"
output.export(audio_name, format="wav")
print("Audio done")

#Video export
video_name = [f for f in os.listdir("Video")]
video_name = video_name[0]
result_name = os.path.splitext(video_name)[0]
cmd = '{} -y -loglevel fatal -i {} -i Video/{} -c:a pcm_s16le Result/{}.mov'.format(FFMPEG_BIN, audio_name, video_name, result_name+"_crop"+crop_value)
subprocess.run(cmd)
print("Video done")