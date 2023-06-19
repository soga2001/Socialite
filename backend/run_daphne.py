import sys

if __name__ == '__main__':
    # insert here whatever commands you use to run daphne
    sys.argv = ['daphne', 'backend.asgi:application']
    from daphne.cli import CommandLineInterface

    CommandLineInterface.entrypoint()
