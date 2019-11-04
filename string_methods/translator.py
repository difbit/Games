
string_to_solve = """g fmnc wms bgblr \
rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq \
ypc dmp. bmgle gr gl zw fylb gq glcddgagclr \
ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle \
qrpgle.kyicrpylq() gq pcamkkclbcb. \
lmu ynnjw ml rfc spj."""

abc = "abcdefghijklmnopqrstuvwxyz"

def solver(solve_this):
    index_collection = []
    solve_this = list(solve_this)
    for str in solve_this:
        if abc.find(str) != -1:
            spot = abc.find(str)
            if abc[spot] == 'y':
                spot = -2
            elif abc[spot] == 'z':
                spot = -1
            str = abc[spot + 2]
        index_collection.append(str)
    index_collection = ''.join(index_collection)
    print index_collection
    index_collection = []

solver(string_to_solve)
solver('map')
