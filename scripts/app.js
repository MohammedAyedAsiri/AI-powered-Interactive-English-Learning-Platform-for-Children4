document.getElementById("recordBtn").addEventListener("click", function() {
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
        const mediaRecorder = new MediaRecorder(stream);
        let audioChunks = [];

        mediaRecorder.start();
        this.textContent = "Recording... Click to stop.";
        
        mediaRecorder.ondataavailable = function(event) {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = function() {
            const audioBlob = new Blob(audioChunks);
            // Call function to evaluate pronunciation
            evaluatePronunciation(audioBlob);
        };

        this.onclick = function() {
            mediaRecorder.stop();
            this.textContent = "🎤 Speak Now";
        };
    })
    .catch(function(error) {
        document.getElementById("feedback").textContent = "Error accessing the microphone: " + error.message;
    });
});

function evaluatePronunciation(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob);

    fetch('/api/evaluate_pronunciation', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("feedback").innerText = `You said: ${data.spoken}. Accuracy: ${data.accuracy}%`;
    })
    .catch(error => {
        document.getElementById("feedback").innerText = "Error evaluating pronunciation: " + error.message;
    });
}