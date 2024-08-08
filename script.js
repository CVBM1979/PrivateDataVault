document.addEventListener('DOMContentLoaded', () => {
    const tokenUrl = 'http://127.0.0.1:5000/get_token';

    async function getToken() {
        const response = await fetch(tokenUrl);
        const data = await response.json();
        return data.token;
    }

    async function handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) {
            alert('No file selected.');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', file);

        try {
            const token = await getToken();
            const response = await fetch('http://127.0.0.1:5000/upload_file', {
                method: 'POST',
                headers: {
                    'Authorization': `token ${token}`
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            alert('File uploaded successfully');
        } catch (error) {
            console.error('Error uploading file:', error);
            alert('Error uploading file');
        }
    }

    document.getElementById('uploadButton').addEventListener('click', () => {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '*/*';
        fileInput.onchange = handleFileUpload;
        fileInput.click();
    });

    document.getElementById('downloadButton').addEventListener('click', async () => {
        try {
            const token = await getToken();
            const response = await fetch('http://127.0.0.1:5000/download_files', {
                method: 'GET',
                headers: {
                    'Authorization': `token ${token}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const blob = await response.blob();
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'files.zip';
            link.click();
        } catch (error) {
            console.error('Error downloading files:', error);
            alert('Error downloading files');
        }
    });

    document.getElementById('deleteButton').addEventListener('click', async () => {
        try {
            alert('Starting deletion process...');
            const token = await getToken();
            const response = await fetch('http://127.0.0.1:5000/delete_files', {
                method: 'POST',
                headers: {
                    'Authorization': `token ${token}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            alert(`Deletion result: ${JSON.stringify(result)}`);
        } catch (error) {
            console.error('Error deleting files:', error);
            alert(`Error deleting files: ${error.message}`);
        }
    });
});


