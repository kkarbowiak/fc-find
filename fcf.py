import argparse
import os
import os.path
import hashlib


def main():
    parser = get_args_parser()
    args = parser.parse_args()

    source_data = get_files_hashes(args.source)
    target_data = get_files_hashes(args.target)

    source_hashes = set(source_data.keys())
    target_hashes = set(target_data.keys())
    intersection_hashes = source_hashes & target_hashes

    for ih in intersection_hashes:
        print(ih[0:8], source_data[ih], ' -> ', target_data[ih])


def get_args_parser():
    parser = argparse.ArgumentParser(description='File duplicate finder')

    parser.add_argument('source', help='source path')
    parser.add_argument('target', help='target path')

    return parser


def get_files_hashes(path):
    data = {}

    for root, dirs, files in os.walk(path):
        for fn in files:
            fp = os.path.join(root, fn)
            with open(fp, 'rb') as f:
                content = f.read()
                digest = hashlib.sha256(content).hexdigest()
                data[digest] = fp

    return data


if __name__ == '__main__':
    main()
