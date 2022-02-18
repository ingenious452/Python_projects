import argparse
import hashlib
import os.path
import os
import sys

parser = argparse.ArgumentParser(prog='DuplicateFileHandler',
                                 description='Path of the folder in which to check for the duplicates files.')
parser.add_argument('path', nargs='?', type=str, help='Folder path')
args = parser.parse_args()


def get_files(folder, format=''):
    """Print all the file in the directory and the subdirectory with there sizes.
    :folder: str -> path to the directory to search in
    :format: str -> files format to search for.

    :return -> None"""

    file_paths = {}
    for root, _, files in os.walk(folder):
        for file in files:                   # lopping through files list as each iteration contain list of files
            # in directory and subdirectory of the folder
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)

            if format != '':     # check if we have format
                if ''.join(['.', format]) == os.path.splitext(file)[-1]:
                    # create a dict file_size as key and a list of
                    file_paths[file_size] = file_paths.setdefault(
                        file_size, [])
                    # file_path with he same file_size
                    file_paths[file_size].append(file_path)
            else:
                file_paths[file_size] = file_paths.setdefault(file_size, [])
                file_paths[file_size].append(file_path)
    return file_paths


def check_duplicates(file_paths):
    """Calculate hash of all the file with samsize and return files with same size and hashes
    :file_paths: str -> Dict of all file with there size as key i.e {'250': [file paths]}

    :retun: Dict -> all the files with same size and hash.
    """

    for file_size, files in file_paths.items():
        files_hashs = {}
        for file in files:
            md5 = hashlib.md5()
            file_obj = open(file, 'rb')
            for line in file_obj:
                md5.update(line)
            file_hash = md5.hexdigest()
            files_hashs[file_hash] = files_hashs.setdefault(file_hash, [])
            files_hashs[file_hash].append(file)
            file_paths[file_size] = files_hashs

    duplicate_file_paths = {}
    file_count = 0
    for file_size, file_hashes in file_paths.items():
        f_hash = {}
        for file_hash, files in file_hashes.items():
            if len(files) > 1:
                file_count += 1
                f_hash[file_hash] = files
                duplicate_file_paths[file_size] = f_hash
    return file_count, duplicate_file_paths


def show_all(file_paths, sorting):
    file_sorted_size = sorted(file_paths)
    if sorting == 1:
        file_sorted_size = sorted(file_paths, reverse=True)

    for file_size in file_sorted_size:
        print('Size: {} bytes'.format(file_size))
        for file in file_paths[file_size]:
            print(file)
        print()


def show_duplicates(file_paths, sorting):
    file_sorted_size = sorted(file_paths)
    if sorting == 1:
        file_sorted_size = sorted(file_paths, reverse=True)

    file_no = 1
    for file_size in file_sorted_size:
        print('Size: {} bytes'.format(file_size))
        for file_hash, files in file_paths[file_size].items():
            print('Hash: {}'.format(file_hash))
            for file in files:
                print('{}. {}'.format(file_no, file))
                file_no += 1
        print()


def delete_files(duplicate_file_paths, remove_files, sorting):
    file_sorted_size = sorted(duplicate_file_paths)
    if sorting == 1:
        file_sorted_size = sorted(duplicate_file_paths, reverse=True)
    file_no = 1
    removed_size = 0
    for file_size in file_sorted_size:
        for file_hash, files in duplicate_file_paths[file_size].items():
            for file in files:
                if file_no in remove_files:
                    os.remove(file)
                    removed_size += file_size
                file_no += 1

    print('Total freed up space: {} bytes'.format(removed_size))


def main():
    print('Enter file Format:')
    file_format = input()
    fs = get_files(args.path, file_format)

    print('Size of sorting options:')
    print('1. Descending')
    print('2. Ascending')
    print()
    print('Enter a sorting option:')
    order = int(input())

    while order not in [1, 2]:
        print()
        print('Wrong option')
        print()
        print('Enter a sorting option:')
        order = int(input())
    print()
    show_all(fs, order)
    total_duplicate, duplicate_paths = check_duplicates(fs)
    while True:
        print('Check for duplicates?')
        duplicate = input()
        print()
        if duplicate == 'yes':
            show_duplicates(duplicate_paths, sorting=order)
            break
        elif duplicate == 'no':
            break
        else:
            print()
            print('Wrong option')
            print()

    while True:
        print('Delete files?')
        try:
            file_to_delete = [int(file_no) for file_no in input().split(' ')]
        except ValueError:
            print()
            print('Wrong option')
            print()
        else:
            if max(file_to_delete) > total_duplicate * 2:
                print()
                print('Wrong option')
                print()
            else:
                delete_files(duplicate_paths, file_to_delete, sorting=order)
                break

    print()


if args.path == None:
    print('Directory is not specified')
    sys.exit()

if __name__ == '__main__':
    main()
