# https://stackoverflow.com/questions/13549294/get-all-the-layers-in-a-packet
def getlayers(self, pkt):
    layers = []
    counter = 0
    while True:
        layer = pkt.getlayer(counter)
        if not layer:
            break
        layers.append(layer)
        counter += 1
    return layers