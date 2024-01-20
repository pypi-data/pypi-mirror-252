from os.path import abspath, join, dirname
def full_path(filename):
    return abspath(join(dirname(__file__), filename))