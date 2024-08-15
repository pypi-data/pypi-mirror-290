from PIL import Image
from pyzbar.pyzbar import decode
from loguru import logger


def get_url_from_image(image):
    logger.debug(f'Getting data from QRCODE in {image}')
    img = Image.open(image)
    decoded_lst = decode(img)
    logger.debug(f'Found {len(decoded_lst)} urls')
    return decoded_lst[0].data if decoded_lst[0].type == 'QRCODE' else None


if __name__ == "__main__":
    get_url_from_image('IMG_5971.PNG')