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

    if args.difference:
        print_difference(source_hashes, target_hashes, source_data, target_data)


def get_args_parser():
    parser = argparse.ArgumentParser(description='File duplicate finder')

    parser.add_argument('source', help='source path')
    parser.add_argument('target', help='target path')
    parser.add_argument('-d', '--difference', action='store_true', help='show files in source that are not in target')

    return parser


def get_files_hashes(path):
    data = {}

    for root, dirs, files in os.walk(path):
        for fn in files:
            fp = os.path.join(root, fn)
            digest = get_file_hash(fp)
            data[digest] = fp

    return data


def get_file_hash(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        return hashlib.sha256(content).hexdigest()


def print_difference(source_hashes, target_hashes, source_data, target_data):
    print('Source/target difference:')
    difference = source_hashes - target_hashes
    for d in difference:
        print(d[0:8], source_data[d])


if __name__ == '__main__':
    main()
