from fastapi import FastAPI, UploadFile, File
app = FastAPI()

@app.get('/')
def root():
    return {'status':'ok'}

@app.post('/upload')
async def upload(files: list[UploadFile] = File(...)):
    # don't process, just return filenames quickly
    names = [f.filename for f in files]
    return {'status':'ok','uploaded': names}

@app.post('/query')
async def query(question: str):
    return {'source':'min','answer':'This is a test fallback answer.'}
