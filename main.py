from integration import findIntegration
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("url")

    args = parser.parse_args()

    integration = findIntegration(args.url)
    if integration is not None:
        integration.fetchAllSong()
