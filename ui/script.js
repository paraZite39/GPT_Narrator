window.addEventListener('load', async () => {
    const video = document.getElementById('webcam');
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (error) {
        console.error('Error accessing webcam:', error);
    }
});

// Example function to handle playing narration audio
function playNarration(audioUrl) {
    const audioPlayer = document.getElementById('narrationAudio');
    audioPlayer.src = audioUrl;
    audioPlayer.play();
}

// Add your logic here to connect with your backend
let userId = Math.floor(Math.random() * 1000000);

document.getElementById('captureFrame').addEventListener('click', async () => {
    const video = document.getElementById('webcam');
    if (video.srcObject) {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const b64String = canvas.toDataURL('image/jpeg').split(',')[1]; // Get base64 string

        const narrator = document.getElementById('voiceSelect').value;
        const payload = {
            user_id: userId,
            b64_string: b64String,
            narrator: narrator
        };

        try {
            const audioPlayer = document.getElementById('audioPlayer');
            const response = await fetch('http://127.0.0.1:8000/narrate_stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                audioPlayer.src = URL.createObjectURL(await response.blob());
                audioPlayer.play();
            } else {
                console.error('Stream not available');
            }
        } catch (error) {
            console.error('Error sending frame:', error);
        }
    } else {
        console.error('Webcam is not active');
    }
});


document.getElementById('clearOutput').addEventListener('click', () => {
    document.getElementById('streamOutput').value = ''; // Clear the textarea
});