import qrcode
import re
""" 
***********************************************************************************
* file name : generator.py
* description : contains all the qrcode functions
* version : 1.0

***********************************************************************************
                ******Change History*******

WHO                  WHEN              Version           Change
---------------      -------------     --------          ------------
goodnessglister      30-JAN-2025       1.0               initial 

***********************************************************************+************

 """
def create(link,fill_color='black'):
	
	"""
    ******************************************************************************
    * function or method :create
    * description : Generates qr code from a url or any link
    * version :1.0
    ******************************************************************************
                        ****   Change History ****

    WHO                  WHEN              Version           Change
    ---------------      -------------     --------          ------------
    goodnessglister      30-JAN-2025       1.0               initial 
    ***********************************************************************+************

    """
		
	qr=qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=2
		)
	qr.add_data(link)
	qr.make(fit=True)
	img=qr.make_image(fill_color=fill_color,back_color='white')
	return img




def create_email(mail_link,fill_color='black'):
	"""
    ******************************************************************************
    * function or method :create_email
    * description : Generates a qr code but for emails
    * version :1.0
    ******************************************************************************
                        ****   Change History ****

    WHO                  WHEN              Version           Change
    ---------------      -------------     --------          ------------
    goodnessglister      30-JAN-2025       1.0               initial 
    ***********************************************************************+************

    """
	qr=qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=2
		)
	
	data=f"mailto:{mail_link}"
	qr.add_data(data)
	qr.make(fit=True)

	img=qr.make_image(fill_color=fill_color,back_color='white')

	return img


def create_phone(phone_number,fill_color='black'):
	"""
    ******************************************************************************
    * function or method : create_phone
    * description : Generates a direct all acess to a phone number
    * version :1.0
    ******************************************************************************
                        ****   Change History ****

    WHO                  WHEN              Version           Change
    ---------------      -------------     --------          ------------
    goodnessglister      30-JAN-2025       1.0               initial 
    ***********************************************************************+************

    """
	qr=qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=2
		)
	
	data=f"tel:{phone_number}"

	qr.add_data(data)
	qr.make(fit=True)
	img=qr.make_image(fill_color=fill_color,back_color='white')

	return img

def generate(data,fill_color='black'):
    """
    ******************************************************************************
    * function or method : gen
    * description : using the three fucntions to generate a  type of url 
      depending on the users type of input
    users
    * version :1.0
    ******************************************************************************
                        ****   Change History ****

    WHO                  WHEN              Version           Change
    ---------------      -------------     --------          ------------
    goodnessglister      30-JAN-2025       1.0               initial 
    ***********************************************************************+************

    """
    
    email=r"[a-zA-Z0-9]+@[a-zA-Z0-9]+.[a-zA-Z]+"
    phone=r"\+[0-9]+"
    url=r"[a-zA-Z0-9]+.[a-zA-Z]"
    if bool(re.match(email,data)):
        img=create_email(data,fill_color)
    elif re.match(phone,data):
        img=create_phone(data,fill_color)
    elif re.match(url,data):
        img=create(data,fill_color)
    return img