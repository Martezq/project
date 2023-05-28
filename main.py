import os

def should_skip_directory(directory):
    # Skip hidden directories or virtual environment directories
    return directory.startswith('.') or directory == 'venv'

def print_directory_tree(start_path):
    for root, dirs, files in os.walk(start_path):
        # Remove skipped directories from the dirs list (modifies os.walk behavior)
        dirs[:] = [d for d in dirs if not should_skip_directory(d)]

        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            print(f"{sub_indent}{file}")

# Example usage
print_directory_tree('D:\Python\PycharmProjects\kazkas')
