#!/usr/bin/env python

from __future__ import print_function

import base64
import os
import subprocess
import sys
import tempfile

class UnsupportedPlatformError(RuntimeError):
    pass

def clipboard_put(data):
    if sys.platform == 'darwin':
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        p.stdin.write(data)
        p.stdin.close()
        p.communicate()
    elif sys.platform == 'msys':
        with open('/dev/clipboard', 'wb') as f:
            return f.write(data)
    else:
        raise UnsupportedPlatformError(
                         'Putting on {} is not supported'.format(sys.platform))

def clipboard_get():
    if sys.platform == 'darwin':
        p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
        return p.communicate()[0]
    elif sys.platform == 'msys':
        with open('/dev/clipboard', 'rb') as f:
            return f.read()
    else:
        raise UnsupportedPlatformError(
                         'Getting on {} is not supported'.format(sys.platform))

def usage(file):
    print('''Usage: {0} [-h] <subcommand>
  put <revspec>  Put the specified <revspec> into the clipboard
  get            Fetch the contents of the clipboard'''.format(sys.argv[0]),
          file=file)

def put(revspec):
    cmd = ['git', 'bundle', 'create', '-'] + revspec
    git = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out = git.communicate()[0]
    if git.returncode:
        raise subprocess.CalledProcessError(git.returncode, ' '.join(cmd))
    clipboard_put(base64.b64encode(out))

def get():
    data = base64.b64decode(clipboard_get())

    temp, tempname = tempfile.mkstemp()
    os.write(temp, data)

    subprocess.check_call(['git', 'fetch', tempname])

    os.remove(tempname)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        usage(sys.stderr)
        sys.exit(-1)

    try:
        if sys.argv[1] == 'put':
            put(sys.argv[2:])
        elif sys.argv[1] == 'get':
            get()
        elif sys.argv[1] == '-h':
            usage(sys.stdout)
            sys.exit(0)
        else:
            usage(sys.stderr)
            sys.exit(-1)
    except UnsupportedPlatformError as e:
        print(e.message, file=sys.stderr)
        sys.exit(-1)
    except subprocess.CalledProcessError:
        sys.exit(-1)

