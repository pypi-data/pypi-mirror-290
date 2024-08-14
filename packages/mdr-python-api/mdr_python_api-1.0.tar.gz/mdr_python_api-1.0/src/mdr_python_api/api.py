from typing import Tuple
import json

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 9393  # Port to listen on (non-privileged ports are > 1023)
NUM_PROTOCOL_START_BYTES = 4
MOCK = False

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

'''
Initialize server connection
'''
def init(new_host):
    global HOST
    HOST = new_host


def init(new_host, new_port):
    global HOST
    global PORT
    HOST = new_host
    PORT = new_port

def enable_mock():
    global MOCK
    MOCK = True
    
def send_data(raw_data):
    if MOCK:
        return
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        b = bytearray()
        b.extend(map(ord, raw_data))
        n = len(raw_data)
        nb = (n).to_bytes(NUM_PROTOCOL_START_BYTES, byteorder='big')
        s.send(nb)
        s.sendall(b)



def read_string():
    if MOCK:
        return
    result_string = ""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while 1:
            data = s.recv(100)
            if not data:
                break
            result_string += data.decode("utf-8")
        s.close()
        print(f"read string {read_string}")
    return result_string

'''
    Register dependencies for a given dataset. 
    label and version determines the dataset for which we are adding dependencies.
    `dependencies` is an array of dependent datasets passed a tuples of label and version
    [(l1, v1), ..., (ln, vn)]
    `input_dep` is a flag determining if this is input or output dependency.
'''
def add_dependencies(label: str, version: str, dependencies: list[Tuple[str, str]], input_dep: bool):
    if MOCK:
        return

    deps = ""
    for (name, version) in dependencies:
        deps += f"{name}:{version}"
    command = "INPUT" if input_dep == True else "OUTPUT"
    raw_data = f"{command}:{label}:{version}:{deps}"
    send_data(raw_data)


'''
    Adding or updating meta data into the server
    label is the MD label
    version is the version of the MD
    md is the MD itself as a single python object (enclosed in {}). If a 
    meta data with the current label and version exists, the function
    simply updates the exisiting MD. Otherwise, it adds the new MD to DB.
    Returns the object unique ID of the new (updated) record.
'''


def register_meta_data(label: str, version: str, owner: str, url:str, md: str) -> str:
    if MOCK:
        if not is_json(md):
            raise Exception("MetaData has to be a json object") 
        return
    import socket

    raw_data = f"UPDATE:{label}:{version}:{owner}:{url}:{md}"
    result_string = ""

    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        b = bytearray()
        b.extend(map(ord, raw_data))
        n = len(raw_data)
        nb = (n).to_bytes(NUM_PROTOCOL_START_BYTES, byteorder='big')
        s.send(nb)
        s.sendall(b)
        while 1:
            data = s.recv(100)
            if not data:
                break
            result_string += data.decode("utf-8")
        s.close()
    print(f"obj id {read_string}")
    return result_string
    
def search_MD(search_string, dependencies):
    if MOCK:
        return {}
    
    import socket

    raw_send_req_data = f"SEARCH:label:{search_string}::"
    if dependencies:
        raw_send_req_data = f"DEPENDENCY:label:{search_string}::"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        b = bytearray()
        b.extend(map(ord, raw_send_req_data))
        n = len(raw_send_req_data)
        nb = (n).to_bytes(NUM_PROTOCOL_START_BYTES, byteorder='big')
        s.send(nb)

        s.sendall(b)
        result_string = ""
        while 1:
            data = s.recv(1024)
            if not data:
                break
            result_string += data.decode("utf-8")
        s.close()
    delimiter = chr(0xFF)
    results = result_string.split(delimiter)
    print(f"search size {len(results)}")
    return results


'''
    The function returns a list of matching data 
    MDs in the following format [<header><MD>, ...]
'''
def search_meta_data(search_string: str):
    return search_MD(search_string, False)
'''
    For each dataset MD, there is a separate LOCATOR object that keeps track of
    the relations for that objects (it's input/output MD objects).
    The function returns a list of matching data locators.
    
    Each MD locator have the same label of the corresponding MD with ":-- LOCATOR" suffix 
    An MD locator, keeps track of the inputs and outputs relations of the corresponding
    MD dataset object. Each locator has the same header as the original object and two lists, 
    inputs and outputs. So the result looks similar to this:
    [<name:-- LOCATOR><rest of header><input><output>, ...]
'''
def search_dependencies(search_string: str):
    return search_MD(search_string, True)

'''
   NOT FUNCTIONAL! 
   Transfer data from source dataset to dest dataset.
   source_label, source_version are source_path are the label and version and path in the the source dataset
   dest_label, dest_version are dest_path are the label and version and path in the the destination dataset
'''


def transfer_data(source_label, source_version, source_path, dest_label, dest_version, dest_path):
    import socket

    raw_data = f"TRANSFER:{source_label}:{source_version}:{source_path}:" \
        f"{dest_label}:{dest_version}:{dest_path}"
    send_data(raw_data)
