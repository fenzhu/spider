import os
import shutil
import sys

target = ""


def move_mp4_files(target_directory):
    # Iterate over all directories and subdirectories
    print(f"{target} {target_directory}")
    for root, dirs, files in os.walk(target_directory):
        if target_directory != target:
            for file in files:
                if file.endswith(".mp4"):
                    # Construct full file path
                    file_path = os.path.join(root, file)
                    # Move file to the target directory
                    shutil.move(file_path, target)
                    print(f"Moved: {file_path} to {target_directory}")
        for dir in dirs:
            print(f"go to dir {dir}")
            move_mp4_files(os.path.join(root, dir))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python move.py <directory_path>")
        sys.exit(1)

    target_directory = sys.argv[1]

    if not os.path.isdir(target_directory):
        print(f"The provided path is not a directory: {target_directory}")
        sys.exit(1)
    target = target_directory
    move_mp4_files(target_directory)
