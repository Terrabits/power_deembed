import skrf as rf

def read_s21(filename):
    network = rf.Network(filename)
    return network.f, network.s21.s_db.flatten()
