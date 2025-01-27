import qrcode

def qr_generate(border, fill_color, back_color, link):
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=border,
    )

    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save("qr_code.png")