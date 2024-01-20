import requests
import numpy as np
import base64
from typing import List

from riotee_gateway.packet_model import PacketApiSend
from riotee_gateway.packet_model import PacketApiReceive


def decode_dev_id(dev_id_b64: str):
    return np.frombuffer(base64.urlsafe_b64decode(dev_id_b64), dtype=np.uint16)[0]


def encode_data(data: bytes) -> bytes:
    return base64.urlsafe_b64encode(data)


class GatewayClient(object):
    def __init__(self, host: str = "localhost", port: int = 8000):
        self.__url = f"http://{host}:{port}"

    def convert_dev_id(fn_called):
        """Automatically converts dev_id argument to base64"""

        def _convert_dev_id_wrapped(self, dev_id: int | str, *args):
            if dev_id is None:
                return fn_called(self, None, *args)
            if type(dev_id) is str:
                return fn_called(self, dev_id, *args)
            dev_id_b64 = encode_data(np.uint32(dev_id))
            return fn_called(self, dev_id_b64, *args)

        return _convert_dev_id_wrapped

    def get_devices(self) -> List[str]:
        """Reads the list of all devices from which the gateway has received packets."""
        r = requests.get(f"{self.__url}/devices")
        r.raise_for_status()
        return r.json()

    @convert_dev_id
    def send_packet(self, dev_id: int | str, pkt: PacketApiSend):
        r = requests.post(f"{self.__url}/out/{dev_id}", data=pkt.model_dump_json())
        r.raise_for_status()

    @convert_dev_id
    def send_ascii(self, dev_id: int | str, text: str, pkt_id: int = None):
        if pkt_id is None:
            pkt_id = np.random.randint(0, 2**16)
        pkt = PacketApiSend(data=encode_data(bytes(text, encoding="utf-8")), pkt_id=pkt_id)
        self.send_packet(dev_id, pkt)

    @convert_dev_id
    def get_queue_size(self, dev_id: int | str) -> int:
        """Reads the number of packets in the queue for the corresponding device."""
        r = requests.get(f"{self.__url}/in/{dev_id}/size")
        r.raise_for_status()
        return int(r.json())

    @convert_dev_id
    def get_packet(self, dev_id: int | str, pkt_index: int) -> PacketApiReceive:
        """Retrieves a packet from the gateway's fifo queue."""
        r = requests.get(f"{self.__url}/in/{dev_id}/{pkt_index}")
        r.raise_for_status()

        return PacketApiReceive.from_json(r.json())

    @convert_dev_id
    def delete_packet(self, dev_id: int | str, pkt_index: int):
        """Retrieves a packet from the gateway's fifo queue."""
        r = requests.delete(f"{self.__url}/in/{dev_id}/{pkt_index}")
        r.raise_for_status()
        return r.json()

    @convert_dev_id
    def pop(self, dev_id: int | str) -> PacketApiReceive:
        """Pops the first packet from the gateways' fifo queue for the specified device.."""
        try:
            pkt = self.get_packet(dev_id, 0)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                raise IndexError("No packets in Queue for device")
            raise
        self.delete_packet(dev_id, 0)
        return pkt

    @convert_dev_id
    def pops(self, dev_id: int | str):
        """Pops all packets from the gateway's fifo queue for the specified device."""
        while True:
            try:
                yield self.pop(dev_id)
            except IndexError:
                return

    @convert_dev_id
    def get_packets(self, dev_id: int | str = None) -> List[PacketApiReceive]:
        """Retrieves all packets from all the gateway's fifo queues."""
        if dev_id is None:
            r = requests.get(f"{self.__url}/in/all/all")
        else:
            r = requests.get(f"{self.__url}/in/{dev_id}/all")
        r.raise_for_status()
        return [PacketApiReceive.from_json(json_dict) for json_dict in r.json()]

    @convert_dev_id
    def delete_packets(self, dev_id: int | str = None):
        """Deletes all packets from all the gateway's fifo queues."""
        if dev_id is None:
            r = requests.delete(f"{self.__url}/in/all/all")
        else:
            r = requests.delete(f"{self.__url}/in/{dev_id}/all")
        r.raise_for_status()
        return r.json()
