from mido import MidiFile

# Mido is available on the web ; use pip install mido

#Note that some midi files refused to load with mido due to a non-standard key signature (meta) message.
#I modified the function  MetaSpec_key_signature of the file meta.py as follows (line 17, 18)

# class MetaSpec_key_signature(MetaSpec):
    # type_byte = 0x59
    # attributes = ['key']
    # defaults = ['C']

    # def decode(self, message, data):
        # key = signed('byte', data[0])
        # mode = data[1]
        # if mode not in [0,1]:
            # # Happened in some files : mode is -1 (not found in specs) ==> ignoring
            # mode = 0
        # message.key = _key_signature_decode[(key, mode)]

    # def encode(self, message):
        # key, mode = _key_signature_encode[message.key]
        # return [unsigned('byte', key), mode]

    # def check(self, name, value):
        # if not value in _key_signature_encode:
            # raise ValueError('invalid key {!r}'.format(value))



import argparse
import glob
import os.path

def detune_file(filename_in, filename_out, shift):
    mid = MidiFile(filename_in)
    def detune(msg, shift):
        if not msg.is_meta:
            if msg.type in ['note_off', 'note_on', 'polytouch']:
                msg.note += shift
        return msg

    for i, track in enumerate(mid.tracks):
        for msg in track:
            msg = detune(msg, -1)
        
    mid.save(filename_out)

def detuned_filename(filename, suffix):
    base, ext = os.path.splitext(filename)
    return base + suffix + ext
    
parser = argparse.ArgumentParser(description="Tool to change pitch of midi files")
parser.add_argument('-s', '--shift', type=int, default='-1', help='pitch shift to apply, e.g. -1 to lower 1/2 tone')
parser.add_argument('-a', '--append', type=str, default="", help='string to append to the filenames')
parser.add_argument('-f', '--force', action='store_true', help='allow in-place conversion (same filename)')
parser.add_argument('file', type=str, nargs='+', help='list of files to convert - wildcards allowed')

cmdlineArgs = parser.parse_args()

filelist = [glob.glob(file) for file in cmdlineArgs.file]
flat_filelist = [item for sublist in filelist for item in sublist]
# remove duplicates
flat_filelist = list(set(flat_filelist))
suffix = cmdlineArgs.append
if suffix == "":
    suffix = "repitch%d" % cmdlineArgs.shift

for file in flat_filelist:
    print("Processing %s ..." % file)
    if cmdlineArgs.force:
        detune_file(file, file, cmdlineArgs.shift)
    else:
        detune_file(file, detuned_filename(file, suffix), cmdlineArgs.shift)
    print(" done.")
    