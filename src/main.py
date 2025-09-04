from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import os
import datetime

app = FastAPI()
true_access_code = "20"
pinned_files = {}

@app.get("/")
async def read_root():
    return {"message": "Hello, World(Report Servers)!"}


def sanatize_path(name: str) -> str:
    text = ""
    used_period = False
    for a in name:
        if a.isalnum() or a == "_" or (a == "." and not used_period):
            if a == ".":
                used_period = True
            text += a
        else:
            break
    return text


def ensure_dir(name: str): 
    safe_name = sanatize_path(name)
    if not os.path.isdir(safe_name):
        os.mkdir(safe_name)
        print(f"Made project dir: {safe_name}")


def gen_resp_message(text: str): 
    return {"message": text}

@app.post("/message/")
async def report_message(access_code: str = Form(...), project: str = Form(...), message: str = Form(...)):
    if access_code == true_access_code:
        safe_project_name = sanatize_path(project)
        ensure_dir(safe_project_name)
        with open(f"{safe_project_name}/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w") as f:
            f.write(message)
        return gen_resp_message("ok")
    else:
        return gen_resp_message("error")


@app.post("/file/")
async def report_file(file: UploadFile, access_code: str = Form(...), project: str = Form(...)):
    if access_code == true_access_code:
        safe_project_name = sanatize_path(project)
        ensure_dir(safe_project_name)
        with open(f"{safe_project_name}/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}", "wb") as f:
            content = await file.read()
            f.write(content)
        return gen_resp_message("ok")
    else:
        return gen_resp_message("error")

@app.get("/view/{project_name}")
async def view_project(project_name: str):
    def gen_line(file: str):
        link_part = f'<a href="/download/{safe_project_name}/{file}">{file}</a>'
        # script_part = f"() => window.location.href = '/download/{safe_project_name}/{file}'"
        delete_script = f"fetch('/delete/{safe_project_name}/{file}/{true_access_code}', {{ method: 'POST' }}).then(() => window.location.reload())"
        delete_button = f'<button onClick="{delete_script}">Delete</button>'
        pin_script = f"fetch('/pin_file/{safe_project_name}/{file}/{true_access_code}', {{ method: 'POST' }}).then(() => window.location.reload())"
        pin_button = f'<button onClick="{pin_script}">Pin</button>'
        if safe_project_name in pinned_files and pinned_files[safe_project_name] == os.path.join(safe_project_name, file):
            pin_script = ""
            pin_button = ""
        return f'<li>{link_part}{delete_button}{pin_button}</li>'

    safe_project_name = sanatize_path(project_name)
    if os.path.isdir(safe_project_name):
        files = os.listdir(safe_project_name)
        files.sort()
        
        return HTMLResponse(
            content=f"""
            <html>
                <head>
                    <title>Project: {safe_project_name}</title>
                </head>
                <body>
                    <h1>Files in Project: {safe_project_name}</h1>
                    <ul>
                        {"".join(gen_line(file) for file in files)}
                    </ul>
                </body>
            </html>
            """,
            status_code=200
        )
    else:
        return {"message": "Project not found"}
    

@app.get("/download/{project_name}/{file_name}")
async def download_file(project_name: str, file_name: str):
    safe_project_name = sanatize_path(project_name)
    safe_file_name = sanatize_path(file_name)
    file_path = os.path.join(safe_project_name, safe_file_name)
    
    # print(f"download path: {file_path}")
    if os.path.isfile(file_path):
        return FileResponse(file_path, media_type='application/octet-stream', filename=safe_file_name)
    else:
        return {"message": "File not found"}


# I don't like this inconsistency here
@app.post("/delete/{project_name}/{file_name}/{access_code}")
async def delete_project(project_name: str, file_name: str, access_code: str):
    if access_code == true_access_code:
        safe_project_name = sanatize_path(project_name)
        safe_file_name = sanatize_path(file_name)
        file_path = os.path.join(safe_project_name, safe_file_name)
        
        if os.path.isfile(file_path):
            os.remove(file_path)
            return gen_resp_message("File deleted successfully")
        else:
            return gen_resp_message("File not found")


@app.post("/pin_file/{project_name}/{file_name}/{access_code}")
async def pin_file(project_name: str, file_name: str, access_code: str):
    if access_code == true_access_code:
        safe_project_name = sanatize_path(project_name)
        safe_file_name = sanatize_path(file_name)
        file_path = os.path.join(safe_project_name, safe_file_name)

        if os.path.isfile(file_path):
            pinned_files[safe_project_name] = file_path
            return gen_resp_message("File pinned successfully")
        else:
            return gen_resp_message("File not found")
    else:
        return gen_resp_message("error")


@app.get("/pinned_file/{project_name}")
async def get_pinned_file(project_name: str):
    if project_name in pinned_files and os.path.isfile(pinned_files[project_name]):
        return FileResponse(pinned_files[project_name], media_type='application/octet-stream', filename=os.path.basename(pinned_files[project_name]))
    else:
        return {"message": "No pinned file found"}
