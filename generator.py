import qrcode
def create(link):
		
	qr=qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=2
		)
	qr.add_data(link)
	qr.make(fit=True)
	img=qr.make_image(fill_color='black',back_color='white')
	return img

# def create(link,fc,bc):
# 	qr=qrcode.QRcode(
# 		version=1,
# 		error_correction=qrcode.constants.ERROR_CORRECT_L,
# 		box_size=10,
# 		border=2
# 		)
# 	qr.add_data(link)
# 	qr.make(fit=True)
# 	img=qr.make_image(fill_color=fc,back_color=bc)
# 	return img
