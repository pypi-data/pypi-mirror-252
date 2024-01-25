import subprocess
import pkg_resources
import argparse

def get_top_level_packages():
    # Get a list of all installed packages
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]

    # Filter top-level packages
    top_level_packages = set()
    for package in installed_packages:
        # use pip show to get package details
        result = subprocess.run(['pip', 'show', package], capture_output=True)
        try:
            output = result.stdout.decode('utf-8')
        except UnicodeDecodeError:
            # Handle decoding errors, e.g., replace invalid characters
            output = result.stdout.decode('utf-8', errors='replace')

        # Check if 'Required by' line is empty
        if 'Required-by:' in output:
            required_by = output.split('Required-by:')[1].split('\n')[0].strip()
            version = output.split('Version:')[1].split('\n')[0].strip()
            if not required_by:
                top_level_packages.add(package + '==' + version)

    return top_level_packages

def create_requirements_txt(top_level_packages, output_file='requirements.txt'):
    with open(output_file, 'w') as file:
        for package in sorted(top_level_packages):
            file.write(f"{package}\n")

def main():
    parser = argparse.ArgumentParser(description='Filter top-level dependencies from a requirements file.')
    parser.add_argument('file', help='Input requirements file to clean')

    args = parser.parse_args()
    input_file = args.file

    top_level_packages = get_top_level_packages()

    create_requirements_txt(top_level_packages)

if __name__ == "__main__":
    main()