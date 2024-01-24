import numpy as np
from cc.udp import UDP

rx_addr = ("0.0.0.0", 8010)
tx_addr = ("127.0.0.1", 8081)
udp_comm = UDP(recv_addr=rx_addr, send_addr=tx_addr)

while True:
    udp_comm.sendNumpy(np.random.rand(10))
    print("send")
    print(udp_comm.recvNumpy(timeout=None))


