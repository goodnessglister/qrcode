""" 
	* file_name :main.py
	* description : Everything about the app happens on the main.py there is no need to create
				a folder for the processus to generate the qr codes 
	* version :1.0
	

"""
import tempfile
import uvicorn
<<<<<<< HEAD
import qrcode
from fastapi import FastAPI,Request,Form,File,UploadFile
=======
import asyncio
from fastapi import FastAPI,Request,Form,File,UploadFile,HTTPException
>>>>>>> a79f110 (Updated version after completing functions)
#Using it as a middleware to pass html response
from fastapi.responses import HTMLResponse
#FAst api file response
from fastapi.responses import FileResponse
#Used to redirect to another page
from fastapi.responses import RedirectResponse
#Used to stream the files back to the user
from fastapi.responses import StreamingResponse
#The jinja2 templates
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from io import BytesIO
from PIL import Image
import generator as gen
import os
import yt_dlp
import functions as fn


templates=Jinja2Templates(directory='templates')

#Creating an instance of the fastapi
app=FastAPI()


# ✅ Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Allow all origins (change to specific domains for security)
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # ✅ Allow all headers
)

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
async def create(request:Request,link:str=Form(...),color=Form(...)):
	""""
	* method : create
	* description : creates our qr code , saves in in our folde then send it to the
					download page ready to download
	"""
	
	##Create a temporary file with the tempfile theb save our png
	#temp_file=tempfile.NamedTemporaryFile(dir=custom_dir,delete=False,suffix='.png')
	img=gen.generate(link,color)
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
	image=BytesIO(file_path)

	if os.path.exists(file_path):
		response= StreamingResponse(image, media_type="image/png", headers={
		"Content-Disposition":f"attachment;filename={file_name}"})
		os.remove(file_path)
		return response

	raise HTTPException(status_code=404, detail="File not found")


@app.post('/cancel/{file_name}')
async def cancel(file_name:str):
	"""
	* method : cancel
	* description : api call to cancel download of the qrcode  and return to the home page
	"""
	file_path=f"{QR_CODE_DIR}/{file_name}"
	os.remove(file_path)
	
#Load page toCompress files or reduce the size of a file
@app.get('/compress')
async def compress(request:Request):
	"""
	* method : cancel
	* description : api call to cancel download of the qrcode  and return to the home page
	"""
	
	return templates.TemplateResponse('compress.html',{'request':request,'name':'QR CODE GENERATOR'})

@app.post('/compress/')
async def compress_img(file:UploadFile=File(...),percentage:int=Form(...)):
	try:
		
		content=await file.read()
		
		#Process the image 
		temp_buffer=fn.compress_image(content,percentage)
	
		#Stream back the image for download to the client
		return StreamingResponse(temp_buffer,media_type='img/png',headers={
		"Content-Disposition": f"attachment; filename=compressed_{file.filename}"
		})
	except Exception as e:
		
		raise HTTPException(status_code=500, detail=str(e))


	

# Load page to convert files from pdf to word and word to pdf img to pdf pdf to img
@app.get('/convert')
async def convert(request:Request):
	return templates.TemplateResponse('download_vid.html',{'request':request,'name':'QR CODE GENERATOR'})


#Load page to download a video or image using a  link
@app.get('/download_vid')
async def download_vid(request:Request):
	return templates.TemplateResponse('download_vid.html',{'request':request})

#Fucntioon called to download a video using a link
@app.post('/download_vid')
async def get_vid(link:str=Form(...),quality:str=Form(...)):
	#Create an auxilary storage
	auxilary=BytesIO()

	#Put the downloaded video into the auxillary storage
	auxilary=fn.download_video(link)

	#Stream the video back to the user as a download

	return StreamingResponse(
		auxilary,
		media_type='',
		headers={"content-Disposition":f"attachment; filename=downloaded_{link}"}
	)

	
########################Trial section


def download_video_sync(url: str, output_path: str, quality: int):
    """
    Blocking function that downloads a video from the given URL using yt-dlp.
    The format option is set so that only videos with a maximum height less than or equal to 'quality'
    are chosen. It then saves the video to output_path.
    """
    # Build a format filter: choose the best video stream with height <= quality, combined with the best audio.
    format_filter = f"bestvideo[height<={quality}]+bestaudio/best"
    ydl_opts = {
        "outtmpl": output_path,           # Save video to the temporary file.
        "format": format_filter,            # Use the quality filter.
        "noplaylist": True                  # Download only a single video.
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.post("/download-video/")
async def download_video( url: str = Form(...),quality: int = Form(...)):
    """
    Asynchronous endpoint that downloads a video from the provided URL using the specified maximum quality.
    It creates a temporary file for the download, offloads the blocking download function to a background thread,
    reads the file into a BytesIO buffer, deletes the temporary file, and streams the video back to the client.
    """
    # Create a temporary file; delete=False so we can remove it manually later.
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        temp_filename = tmp_file.name

    # Run the blocking download in a background thread.
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, download_video_sync, url, temp_filename, quality)

    # Read the downloaded video file into memory.
    with open(temp_filename, "rb") as f:
        video_bytes = f.read()
	

	
    
    # Remove the temporary file.
    os.remove(temp_filename)

	
    # Wrap the video data in a BytesIO buffer.
    video_buffer = BytesIO(video_bytes)
	
    video_buffer.seek(0)

	
    # Return the video as a StreamingResponse so the client can download it.
    return StreamingResponse(
        video_buffer,
        media_type="video/mp4",
        headers={"Content-Disposition": f"attachment; filename=downloaded_video{hash(url)}.mp4"}
    )

# Call to use uvicorn to start and monitor our app on port 8000 and 
if __name__=='__main__':
	#Use this in development
	uvicorn.run('main:app',port=8000,reload=True)
	# use this in production (not to automatically reload the app)
	#uvicorn.run('main:app',port=8000,reload=False)

