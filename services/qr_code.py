import qrcode


def get_qr_code(text: str, file_name: str = "qrcode.png") -> None:
    img = qrcode.make(text)
    img.save(file_name)


get_qr_code(f"https://t.me/Moon_Party_Bot?start={1}")

# for i in range(1, 16):
#     get_qr_code(f"https://t.me/DolinaTransferBot?start={i}",
#                 file_name=f"qrcode_{i}.png")

# with open('qrcode.png', 'wb') as f:
#     f.write(get_qr_code(f"https://t.me/Moon_Party_Bot?start={51.5074}_{-0.1278}"))

# def make_qr_code(text: str) -> BufferedInputFile:
#     img = qrcode.make(text)
#     byte_stream = io.BytesIO()
#     img.save(byte_stream)
#     img_bytes = byte_stream.getvalue()
#     img_send = BufferedInputFile(file=img_bytes, filename="img_1.png")
#     return img_send


# def get_authorization_qr_code(username: str, code: str | int) -> BufferedInputFile:
#     code_text = f"https://t.me/Moon_Party_Bot?start={username}_input_code_{code}"
#     return make_qr_code(code_text)

