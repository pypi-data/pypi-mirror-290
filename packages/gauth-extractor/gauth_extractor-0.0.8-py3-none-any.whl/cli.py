import click
from extractor import extract_data_from_url, extract_from_enc_data
from qrreader import get_url_from_image


@click.command()
@click.option("-f","--file", is_flag=True, default=False)
@click.argument("string", type=str, required=True)
def get_google_auth_keys(file, string):
    '''STRING should be the filename or the otpauth url'''
    print(string)
    url = get_url_from_image(string) if file else string
    print(url)
    data = extract_data_from_url(url)
    print(data)
    extract_from_enc_data(data)


if __name__ == "__main__":
    get_google_auth_keys()
