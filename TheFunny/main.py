#!/usr/bin/python3
import sys
import os

import funcs
from sound_funcs import play_sound_from_text, dump_sounds_to_file


from util import *


def get_text(argv):
	if not sys.stdin.isatty():
		return funcs.fromstdin(sys.stdin)

	if len(argv.args) < 1:
		print("Usage: thefunny <file>")
		return

	if os.path.exists(argv[0]):
		return funcs.fromfile(os.path.abspath(argv[1]))

	return funcs.fromargs(*argv.args)



def main(argv):
	text = get_text(argv)

	out_start = argv.flagstart("-o", "--out", val_sep="=")
	if out_start is not None:
		dump_sounds_to_file(text, out_start)
	elif argv.flagged("-o", "--o"):
		dump_sounds_to_file(text, "out.wav")
	else:
		play_sound_from_text(text)



if __name__ == '__main__':
	main(Arguments(sys.argv))
