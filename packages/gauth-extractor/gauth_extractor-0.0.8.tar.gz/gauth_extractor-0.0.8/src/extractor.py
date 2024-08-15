import base64
from loguru import logger
import protobuff.gauth_pb2 as pb
from urllib import parse
from google.protobuf.json_format import MessageToDict
from rich import print

def extract_from_enc_data(encoded_data):
    logger.debug(f"Extracting from {encoded_data}")
    data = base64.b64decode(encoded_data.replace(' ', '+'), validate=True)
    logger.debug(f"base 64 decoded: {data}")
    message = pb.MigrationPayload()
    logger.debug(f"Parsing from data")
    message.ParseFromString(data)
    logger.debug(f"extracted {message.otp_parameters}")
    data_list = MessageToDict(message)['otpParameters']
    for i, j in enumerate(data_list):
        j['secret'] = str(base64.b32encode(message.otp_parameters[i].secret), 'utf-8')
    logger.debug(f"Extracted dictionaries: {data_list}")
    print(data_list)

def extract_data_from_url(url):
    logger.debug(f"Extracting data from {url}")
    p = parse.urlparse(url)
    #TODO: try/cath
    return parse.parse_qs(str(p.query,'utf-8'))['data'][0]


if __name__ == "__main__":
    logger.debug(f"Starting Job")
    data = extract_data_from_url(b'otpauth-migration://offline?data=CicKCvh1mUhv1cwxYNESBHJvb3QaDTE5Mi4xNjguMTAwLjEgASgBMAIQAhgB')
    extract_from_enc_data(data)