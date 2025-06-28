# ReportServer

A simple FastAPI-based server for uploading, downloading, viewing, and deleting project files and messages.

## Features

- Upload text messages to project folders
- Upload files to project folders
- View and download files in a project
- Delete files from a project
- Basic access code protection

## Endpoints

### `GET /`
Returns a welcome test message.

### `POST /message/`
Upload a text message to a project.
- **Form fields:**
    - `access_code`: Access code (default: `20`)
    - `project`: Project name
    - `message`: Message content

### `POST /file/`
Upload a file to a project.
- **Form fields:**
    - `access_code`: Access code (default: `20`)
    - `project`: Project name
    - `file`: File to upload

### `GET /view/{project_name}`
View all files in a project as an HTML page with download and delete options.

### `GET /download/{project_name}/{file_name}`
Download a specific file from a project.

### `GET /delete/{project_name}/{file_name}/{access_code}`
Delete a specific file from a project (requires correct access code).

## Usage

### Run Locally

1. Install dependencies:
        ```bash
        pip install fastapi uvicorn watchfiles python-multipart
        ```
2. Save the server code as `main.py`.
3. Start the server:
        ```bash
        uvicorn main:app --reload
        ```

### Run with Docker

1. Save the provided Dockerfile.
2. Build and run:
        ```bash
        docker build -t reportserver .
        docker run -p 8000:8000 -v $(pwd):/app reportserver
        ```
Or for more ease, just `docker compose up -d`

## Notes

- All files and messages are stored in directories named after the sanitized project name.
- The default access code is `20`. Change `true_access_code` in the code for better security.
- File and project names are sanitized for safety.

## License

MIT License (add your own license if needed).