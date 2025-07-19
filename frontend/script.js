document.addEventListener('DOMContentLoaded', () => {
    const dialectInput = document.getElementById('dialect-input');
    const translateBtn = document.getElementById('translate-btn');
    const resultsSection = document.querySelector('.results-section');
    const originalTranscript = document.getElementById('original-transcript');
    const translatedText = document.getElementById('translated-text');
    const translatedAudio = document.getElementById('translated-audio');
    const downloadTxtBtn = document.getElementById('download-txt-btn');
    const downloadMp3Btn = document.getElementById('download-mp3-btn');

    translateBtn.addEventListener('click', async () => {
        const dialect = dialectInput.value;
        if (!dialect) {
            alert('Please enter some text to translate.');
            return;
        }

        translateBtn.disabled = true;
        translateBtn.textContent = 'Translating...';

        try {
            const response = await fetch('/api/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: dialect }),
            });

            if (!response.ok) {
                throw new Error('Failed to get translation from server.');
            }

            const data = await response.json();

            originalTranscript.textContent = dialect;
            translatedText.textContent = data.translated;
            translatedAudio.src = data.audioUrl;

            resultsSection.style.display = 'block';

        } catch (error) {
            console.error('Translation error:', error);
            alert('An error occurred. Please check the console for details.');
        } finally {
            translateBtn.disabled = false;
            translateBtn.textContent = 'Translate';
        }
    });

    downloadTxtBtn.addEventListener('click', () => {
        const text = translatedText.textContent;
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'translation.txt';
        a.click();
        URL.revokeObjectURL(url);
    });

    downloadMp3Btn.addEventListener('click', () => {
        const audioUrl = translatedAudio.src;
        const a = document.createElement('a');
        a.href = audioUrl;
        a.download = 'translation.mp3';
        a.click();
    });
});