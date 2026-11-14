# files.py - file and path helpers

import os

def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()

def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def append_line(path, line):
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def exists(path):
    return os.path.exists(path)

def is_file(path):
    return os.path.isfile(path)

def is_dir(path):
    return os.path.isdir(path)

def list_files(directory):
    return [f for f in sorted(os.listdir(directory))
            if os.path.isfile(os.path.join(directory, f))]

def list_dirs(directory):
    return [d for d in sorted(os.listdir(directory))
            if os.path.isdir(os.path.join(directory, d))]

def join(a, b):
    return os.path.join(a, b)

def basename(path):
    return os.path.basename(path)

def dirname(path):
    return os.path.dirname(path)

def extension(path):
    return os.path.splitext(path)[1]

def stem(path):
    return os.path.splitext(os.path.basename(path))[0]

def size(path):
    return os.path.getsize(path)

def copy(src, dst):
    import shutil
    shutil.copy2(src, dst)

def move(src, dst):
    import shutil
    shutil.move(src, dst)

def remove(path):
    os.remove(path)
