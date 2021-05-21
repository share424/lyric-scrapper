from integration.liriklaguindonesianet import LirikLaguIndonesiaNet
from integration.liriklaguid import LirikLaguId

integrations = [
    LirikLaguIndonesiaNet(),
    LirikLaguId()
]

def findIntegration(url):
    for integration in integrations:
        if(integration.is_mine(url)):
            return integration
    return None

def getIntegrations():
    return integrations