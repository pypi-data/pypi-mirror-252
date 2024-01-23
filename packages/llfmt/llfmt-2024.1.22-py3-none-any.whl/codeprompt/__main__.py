import glob
import sys


def main():
    args = sys.argv[1:]
    paths = [path for pattern in args for path in glob.glob(pattern)]
    paths.sort(key=lambda s: s.split('/'))
    print("\n".join([f"### {path} ###\n{open(path, 'r').read()}" for path in paths]))


if __name__ == '__main__':
    main()
