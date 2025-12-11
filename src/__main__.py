import sys
from .cli import RainmeasCLI

def main():
    cli = RainmeasCLI()
    exit_code = cli.run(sys.argv[1:])
    sys.exit(exit_code)

if __name__ == "__main__":
    main()