from pydub import AudioSegment
from pydub.playback import play

from time import sleep
from threading import Thread

import json
import os.path


def to_millis(secs):
	return secs*1000


PAUSE_LENGTH_MILLIS = 500
HALF_PAUSE = PAUSE_LENGTH_MILLIS//2
PAUSE = AudioSegment.silent(duration=PAUSE_LENGTH_MILLIS)


def _threadplay(sound):
	Thread(target=play, args=[sound], daemon=True).start()


def _sounds_list(text, remove_null=False):
	arr = []
	for char in text:
		if char in (' ', '\n'):
			arr.append(PAUSE)
			continue

		s = SOUNDS.get(char)
		if s is None:
			if not remove_null:
				arr.append(SOUNDS.get(char))
		else:
			arr.append(SOUNDS.get(char))

	return arr


def play_sound_from_text(text):
	sounds_list = _sounds_list(text, remove_null=True)

	for s in sounds_list:
		if s is PAUSE:
			play(PAUSE)

		if s is not None:
			_threadplay(s)
			sleep(HALF_PAUSE/1000)
		else:
			print(f"Invalid character {char.__repr__()}")


def dump_sounds_to_file(text, path):
	sounds = _sounds_list(text)
	assert len(sounds) > 0

	sounds_len = 0
	for s in sounds:
		sounds_len += HALF_PAUSE if s is not PAUSE else PAUSE_LENGTH_MILLIS
	sounds_len += len(sounds[-1]) + HALF_PAUSE

	start = AudioSegment.silent(sounds_len)

	ov_incr = HALF_PAUSE
	overlay_pos = -ov_incr

	for s in sounds:
		overlay_pos += ov_incr

		if s is PAUSE:
			start += PAUSE
			overlay_pos += PAUSE_LENGTH_MILLIS
			continue

		start = start.overlay(s, position=overlay_pos)

	start.export(path, format="wav")


SOUNDS = {}

def _init_sounds():
	soundspath = "sfxmap.json"

	FILE = open(soundspath, "rb")
	cfg = json.loads(FILE.read(), strict=False)
	FILE.close()

	global SOUNDS
	for k, v in cfg.items():
		p = "sfx/" + v

		assert os.path.exists(p), f"Config error: {k.__repr__()} does not exist, path {p.__repr__()} is not a real path"
		SOUNDS[k] = AudioSegment.from_wav(p)



_init_sounds()
