import argparse
import os
import os.path
import hashlib


def main():
    parser = argparse.ArgumentParser(description='File duplicate finder')

    parser.add_argument('source', help='source path')
    parser.add_argument('target', help='target path')

    args = parser.parse_args()

    source_data = {}
    target_data = {}

    for directory, subdirs, files in os.walk(args.source):
        for fn in files:
            fp = os.path.join(directory, fn)
            with open(fp, 'rb') as f:
                content = f.read()
                digest = hashlib.sha256(content).hexdigest()
                source_data[digest] = fp

    for directory, subdirs, files in os.walk(args.target):
        for fn in files:
            fp = os.path.join(directory, fn)
            with open(fp, 'rb') as f:
                content = f.read()
                digest = hashlib.sha256(content).hexdigest()
                target_data[digest] = fp

    for sd in source_data.items():
        print(sd)
    for td in target_data.items():
        print(td)

    source_hashes = set(source_data.keys())
    target_hashes = set(target_data.keys())
    intersection_hashes = source_hashes & target_hashes

    for ih in intersection_hashes:
        print(ih[0:8], source_data[ih], ' -> ', target_data[ih])


if __name__ == '__main__':
    main()
