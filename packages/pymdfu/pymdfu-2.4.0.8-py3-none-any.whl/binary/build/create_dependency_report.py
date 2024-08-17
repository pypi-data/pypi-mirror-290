"""
Create a dependency report from pip installation log
"""
import sys

LOOKUP_STRING = "Successfully installed"

if len(sys.argv) != 3:
    print("Required arguments:")
    print("  Input file: pip install log file")
    print("  Output file: file to write the dependency report to")
    sys.exit(1)

inputfile = sys.argv[1]
outputfile = sys.argv[2]

with open(inputfile, 'r', encoding='utf-8') as logfile:
    loglines = logfile.readlines()

for logline in loglines:
    if LOOKUP_STRING in logline:
        packages = logline.split(LOOKUP_STRING)[1]
        packages = packages.replace(' ', '\n')
        with open(outputfile, 'w', encoding='utf-8') as dependencyfile:
            dependencyfile.write(packages)
            print(f"Wrote package list with versions to {outputfile}")
            sys.exit(0)

print("ERROR: Could not find package versions in logfile")
sys.exit(2)

