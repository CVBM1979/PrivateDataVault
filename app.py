from flask import Flask, request, jsonify, send_file
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS
import base64

app = Flask(__name__)
load_dotenv()  # Carrega variáveis do arquivo .env

# Configurar CORS para permitir requisições de qualquer origem
CORS(app, resources={r"/*": {"origins": "*"}})

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'CVBM1979'
REPO_NAME = 'PrivateDataVault'
BRANCH_NAME = 'main'  # Atualizado para o branch main

@app.route('/delete_files', methods=['POST'])
def delete_files_from_branch():
    try:
        files_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/download?ref={BRANCH_NAME}'
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}

        if not GITHUB_TOKEN:
            app.logger.error("No GitHub token found")
            return jsonify({"error": "No GitHub token found"}), 500

        response = requests.get(files_url, headers=headers)

        if response.status_code == 404:
            app.logger.info("No files found to delete (directory does not exist)")
            return jsonify({"status": "success", "message": "No files found to delete (directory does not exist)"})

        response.raise_for_status()

        files = response.json()
        app.logger.info(f"Files response: {files}")

        if not files or (isinstance(files, list) and len(files) == 0):
            app.logger.info("No files found to delete")
            return jsonify({"status": "success", "message": "No files found to delete"})

        for file in files:
            app.logger.info(f"Deleting file: {file['name']} with sha: {file['sha']} at {file['path']}")
            delete_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file['path']}"
            sha = file['sha']
            delete_response = requests.delete(delete_url, headers=headers, json={
                "message": "Deleting file",
                "sha": sha,
                "branch": BRANCH_NAME
            })
            app.logger.info(f"GitHub API response: {delete_response.status_code} - {delete_response.text}")
            delete_response.raise_for_status()
            app.logger.info(f"Deleted file: {file['name']}")

        return jsonify({"status": "success", "message": "All files deleted successfully"})
    except requests.exceptions.RequestException as e:
        app.logger.error(f"RequestException: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Exception: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        content = file.read()
        file_name = file.filename

        upload_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/download/{file_name}'
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Content-Type': 'application/json',
        }

        # Encode the file content in base64
        encoded_content = base64.b64encode(content).decode('utf-8')

        response = requests.put(
            upload_url,
            headers=headers,
            json={
                'message': 'Uploading file',
                'content': encoded_content,
                'branch': BRANCH_NAME
            }
        )
        response.raise_for_status()

        return jsonify({"status": "success", "message": "File uploaded successfully"})
    except requests.exceptions.RequestException as e:
        app.logger.error(f"RequestException: {e}")
        return jsonify({"error": str(e)}), 500
    except UnicodeDecodeError as e:
        app.logger.error(f"UnicodeDecodeError: {e}")
        return jsonify({"error": "Failed to decode file content"}), 500

@app.route('/download_files', methods=['GET'])
def download_files():
    try:
        files_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/download?ref={BRANCH_NAME}'
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}
        response = requests.get(files_url, headers=headers)
        response.raise_for_status()
        files = response.json()

        if not files or (isinstance(files, list) and len(files) == 0):
            app.logger.info("No files found to download")
            return jsonify({"status": "success", "message": "No files found to download"})

        from io import BytesIO
        from zipfile import ZipFile

        buffer = BytesIO()
        with ZipFile(buffer, 'w') as zip_file:
            for file in files:
                file_response = requests.get(file['download_url'])
                file_response.raise_for_status()
                zip_file.writestr(file['name'], file_response.content)

        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='files.zip', mimetype='application/zip')
    except requests.exceptions.RequestException as e:
        app.logger.error(f"RequestException: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Exception: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_token', methods=['GET'])
def get_token():
    if not GITHUB_TOKEN:
        app.logger.error("No GitHub token found")
        return jsonify({"error": "No GitHub token found"}), 500
    return jsonify({"token": GITHUB_TOKEN})

if __name__ == '__main__':
    app.run(debug=True)






