""" 
	* file_name :main.py
	* description : Everything about the app happens on the main.py there is no need to create
				a folder for the processus to generate the qr codes 
	* version :1.0

"""
import tempfile
import uvicorn
import qrcode
from fastapi import FastAPI,Request,Form,File,UploadFile
#Using it as a middleware to pass html response
from fastapi.responses import HTMLResponse
#FAst api file response
from fastapi.responses import FileResponse
#Used to redirect to another page
from fastapi.responses import RedirectResponse
#The jinja2 templates
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import generator as gen
import os


templates=Jinja2Templates(directory='templates')

#Creating an instance of the fastapi
app=FastAPI()


custom_dir='images'

app.mount('/static',StaticFiles(directory='static'),name='static')

# Ensure QR code directory exists
QR_CODE_DIR = "static/qrcodes"
os.makedirs(QR_CODE_DIR, exist_ok=True)

@app.get('/')
async def home(request:Request):
	""""
	* method : home
	* description : Route to load the home page of our app
	"""
	return templates.TemplateResponse('index.html',{'request':request,'name':'QR CODE GENERATOR'})

""" @app.get('/createqr')
async def createqr(file: UploadFile = File(...)):
	return templates.TemplateResponse('download.html',{'request':request,'name':'Agressor'}) """


@app.post('/createqr')
async def create(request:Request,link:str=Form(...)):
	""""
	* method : create
	* description : creates our qr code , saves in in our folde then send it to the
					download page ready to download
	"""
	##Create a temporary file with the tempfile theb save our png
	#temp_file=tempfile.NamedTemporaryFile(dir=custom_dir,delete=False,suffix='.png')
	img=gen.create(link)
	file_name = f"{QR_CODE_DIR}/qrcode_{hash(link)}.png"
	img.save(file_name)


	#img.save(temp_file,format="PNG")
	#print(f"Temporary image saved at: {temp_file.name}")
	
	return templates.TemplateResponse('download.html',{'request':request,'file_name':file_name})
	
	
	""" return templates.TemplateResponse('download.html',{
		'request':request,
		'file_path':temp_file,
		'file_name':os.path.basename(temp_file.name)
		}) """

@app.get('/download/{file_name}')
async def download(file_name:str):
	"""
	* method : download
	* description : api call to initiate the download of the qrcode 
	"""
	#Search for the file path and return 

	file_path=f"{QR_CODE_DIR}/{file_name}"

	if os.path.exists(file_path):
		response= FileResponse(file_path, media_type="image/png", filename=file_name)
	
		return response

	raise HTTPException(status_code=404, detail="File not found")


@app.post('/cancel/{file_name}')
async def cancel(file_name:str):
	"""
	* method : cancel
	* description : api call to cancel download of the qrcode  and return to the home page
	"""

	pass

# Call to use uvicorn to start and monitor our app on port 8000 and 
if __name__=='__main__':
	#Use this in development
	uvicorn.run('main:app',port=8000,reload=True)
	# use this in production (not to automatically reload the app)
	#uvicorn.run('main:app',port=8000,reload=False)

