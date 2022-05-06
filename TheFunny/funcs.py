from sound_funcs import play_sound_from_text


def fromstdin(stdin):
	return stdin.read()

def fromfile(path):
	FILE = open(path, "r")
	text = FILE.read()
	FILE.close()

	return text


def fromargs(*args):
	text = ""
	for a in args:
		text += a
		text += ' '
	return text
