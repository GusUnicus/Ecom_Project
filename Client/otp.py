from pyotp import TOTP
import pyotp
import qrcode
from io import BytesIO
import base64


def get_qr(secret_key,username):
    _uri = generate_provisioning_uri(secret_key,username)
    return generate_qr_code(_uri,username)


def generate_qr_code(uri,username):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")
    image_io = BytesIO()
    path =f"./static/temp/qr_{username}.png"
    qr_image.save(path, format="PNG")
    return 

def generate_provisioning_uri(secret_key, username, issuer_name='Secure Ecom App'):

    return pyotp.TOTP(secret_key).provisioning_uri(name=username,issuer_name=issuer_name)

def verify(secret_key,verification_code):
    totp = pyotp.TOTP(secret_key)
    return totp.verify(verification_code)



