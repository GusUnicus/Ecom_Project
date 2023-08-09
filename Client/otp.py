from pyotp import TOTP
import pyotp, secrets
import time
import qrcode
from io import BytesIO
import base64

# for i in range(10):
#     print(TOTP('base32secret3232').now())
#     time.sleep(5)

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
    path =f"C:/Users/Bedivere/Documents/Programming/SPProject/Ecom_project1/Client/static/temp/qr_{username}.png"
    qr_image.save(path, format="PNG")
    # img.save(image_io, format='PNG')
    # image_io.seek(0)
    
    return #base64.b64encode(image_io.getvalue()).decode("utf-8")

def generate_provisioning_uri(secret_key, username, issuer_name='Secure Ecom App'):
    secret_key=base64.b32encode(secret_key.encode()).decode()
    # print(f"encoded {secret_key=}")
    return pyotp.TOTP(secret_key).provisioning_uri(name=username,issuer_name=issuer_name)

def verify(secret_key,verification_code):
    # secret_key=base64.b32encode(secret_key.encode()).decode()
    # print(f"verify {secret_key=}")
    totp = pyotp.TOTP(secret_key)
    print(f"{totp.now()=}")
    return totp.verify(verification_code)

# get_qr('jN5EOnjs07LBEX4','test01')
# totp = pyotp.TOTP('NJHDKRKPNZVHGMBXJRBEKWBU')
# for i in range(1,100,5):
    
#     print(totp.now())

#     time.sleep(5)

