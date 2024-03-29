from typing import List
from pymilvus import connections, utility, Collection
import logging
import json

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
log_template = "=== {:40} ===\n"
search_latency_log_template = "search latency = {:.4f}s"

with open('settings.json') as f:
    settings = json.load(f)

proxy_ip = settings['proxy_ip']
proxy_port = settings['proxy_port']

def connect_to_milvus(host, port) -> None:
    """ Connect to Milvus server """
    logging.info(log_template.format("start connecting to Milvus"))
    connections.connect(alias=f"default", host=host, port=port)
    logging.info(log_template.format(str(connections.list_connections())))


def disconnect_from_milvus() -> None:
    """ Disconnect from Milvus server. """
    logging.info(log_template.format("Disconnecting from Milvus"))
    connections.disconnect(alias="default")

def list_collections() -> list:
    """ List all collections. """
    
    return utility.list_collections()


def main():
    # connect to Milvus
    connect_to_milvus(proxy_ip, proxy_port)

    # list collections
    print(list_collections())
    
    # disconnect from Milvus
    disconnect_from_milvus()


if __name__ == "__main__":
    main()