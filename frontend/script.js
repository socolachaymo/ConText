document.addEventListener('DOMContentLoaded', () => {
    const inputType = document.getElementById('inputType');
    const textInputSection = document.getElementById('text-input-section');
    const fileInputSection = document.getElementById('file-input-section');
    const recordInputSection = document.getElementById('record-input-section');

    const dialectInput = document.getElementById('dialect-input');
    const fileInput = document.getElementById('file-input');
    const recordBtn = document.getElementById('record-btn');
    const videoPreview = document.getElementById('video-preview');
    
    const translateBtn = document.getElementById('translate-btn');
    const loader = document.getElementById('loader');
    const resultsSection = document.querySelector('.results-section');
    
    const originalTranscript = document.getElementById('original-transcript');
    const translatedText = document.getElementById('translated-text');
    const translatedAudio = document.getElementById('translated-audio');
    const downloadTxtBtn = document.getElementById('download-txt-btn');
    const downloadMp3Btn = document.getElementById('download-mp3-btn');

    let mediaRecorder;
    let recordedChunks = [];

    // --- Input Type Switching ---
    inputType.addEventListener('change', () => {
        textInputSection.classList.remove('active');
        fileInputSection.classList.remove('active');
        recordInputSection.classList.remove('active');

        switch (inputType.value) {
            case 'text':
                textInputSection.classList.add('active');
                break;
            case 'audio':
            case 'video':
                fileInputSection.classList.add('active');
                fileInput.accept = inputType.value === 'audio' ? 'audio/*' : 'video/*';
                break;
            case 'record':
                recordInputSection.classList.add('active');
                break;
        }
    });

    // --- Translation Logic ---
    translateBtn.addEventListener('click', async () => {
        const type = inputType.value;
        let formData = new FormData();
        formData.append('type', type);

        if (type === 'text') {
            if (!dialectInput.value) {
                alert('Please enter some text.');
                return;
            }
            formData.append('text', dialectInput.value);
        } else if (type === 'audio' || type === 'video') {
            if (fileInput.files.length === 0) {
                alert('Please select a file.');
                return;
            }
            formData.append('file', fileInput.files[0]);
        } else if (type === 'record') {
            if (recordedChunks.length === 0) {
                alert('Please record a video first.');
                return;
            }
            const blob = new Blob(recordedChunks, { type: 'video/webm' });
            formData.append('file', blob, 'recorded_video.webm');
        }

        showLoader(true);
        try {
            const response = await fetch('/api/translate', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to get translation.');
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            console.error('Translation error:', error);
            alert(`An error occurred: ${error.message}`);
        } finally {
            showLoader(false);
        }
    });

    // --- Video Recording ---
    recordBtn.addEventListener('click', () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            recordBtn.textContent = 'Start Recording';
            videoPreview.style.display = 'none';
        } else {
            startRecording();
        }
    });

    async function startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            videoPreview.srcObject = stream;
            videoPreview.style.display = 'block';
            videoPreview.play();

            recordedChunks = [];
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };
            mediaRecorder.start();
            recordBtn.textContent = 'Stop Recording';
        } catch (err) {
            console.error("Error accessing webcam:", err);
            alert("Could not access webcam. Please ensure permissions are granted.");
        }
    }

    // --- UI Helper Functions ---
    function showLoader(isLoading) {
        loader.style.display = isLoading ? 'block' : 'none';
        translateBtn.disabled = isLoading;
        translateBtn.textContent = isLoading ? 'Translating...' : 'Translate';
    }

    function displayResults(data) {
        originalTranscript.textContent = data.original || 'N/A';
        translatedText.textContent = data.translated || 'N/A';
        
        if (data.audioUrl) {
            translatedAudio.src = data.audioUrl;
            translatedAudio.parentElement.style.display = 'block';
        } else {
            translatedAudio.parentElement.style.display = 'none';
        }
        
        resultsSection.style.display = 'block';
    }

    // --- Download Buttons ---
    downloadTxtBtn.addEventListener('click', () => {
        const text = translatedText.textContent;
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'translation.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });

    downloadMp3Btn.addEventListener('click', () => {
        const audioUrl = translatedAudio.src;
        if (!audioUrl) return;
        const a = document.createElement('a');
        a.href = audioUrl;
        a.download = 'translation.mp3';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    });
});
