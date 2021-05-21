from integration import getIntegrations
from argparse import ArgumentParser

if __name__ == "__main__":
    integrations = getIntegrations()
    print("Select Lyric Site:")
    for i, integration in enumerate(integrations):
        print(f"{i}. {integration._base_url}")
    index = int(input("Enter lyric site number: "))
    integrations[index].fetchAllSong()
