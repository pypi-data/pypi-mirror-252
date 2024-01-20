from PyConSolv.misc.inputparser import XYZ

if __name__ == '__main__':
    x = XYZ('/home/rat/PycharmProjects/PyConSolv/src/PyConSolv/db/atom-radius.txt',
            '/home/rat/PycharmProjects/PyConSolv/src/PyConSolv/db/metal-radius.txt')
    file = input("file: ")
    x.readXYZ(file)
    x.calculateDistanceMatrix()
    x.generateAdjacencyMatrix()
    x.generateLinkList()
    x.connectedCompponents()
    x.createPDB()
    print("done")