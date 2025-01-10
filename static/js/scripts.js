async function loadFilters() {
    const response = await fetch('/api/filters');
    const filters = await response.json();

    const filtersDisplay = document.getElementById('filters-display');
    filtersDisplay.innerHTML = `<pre>${JSON.stringify(filters, null, 2)}</pre>`;
}

async function loadLogs(logType) {
    const response = await fetch(`/api/logs/${logType}`);
    const logs = await response.json();

    const logsDisplay = document.getElementById('logs-display');
    logsDisplay.innerHTML = `<h3>${logType} Logs</h3><pre>${JSON.stringify(logs.logs || logs, null, 2)}</pre>`;
}

async function loadState() {
    const response = await fetch('/api/activity_tracker');
    const state = await response.json();

    const monitorDisplay = document.getElementById('monitor-display');
    monitorDisplay.innerHTML = `<h3>Activity Tracker</h3><pre>${JSON.stringify(state, null, 2)}</pre>`;
}

async function loadSystemInfo() {
    const response = await fetch('/api/system_monitor');
    const systemInfo = await response.json();

    const monitorDisplay = document.getElementById('monitor-display');
    monitorDisplay.innerHTML = `<h3>System Info</h3><pre>${JSON.stringify(systemInfo, null, 2)}</pre>`;
}

async function changeSource() {
    const source = document.getElementById("source").value;
    const response = await fetch("/set_source", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source })
    });

    if (response.ok) {
        console.log(`Source changed to ${source}`);
        document.getElementById("video-stream").src = "/live_feed?" + new Date().getTime();
    } else {
        console.error("Failed to change source");
    }
}

function showTab(tabId) {
    // Hide all tabs
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach((content) => content.style.display = 'none');

    // Remove active class from all sidebar buttons
    const sidebarButtons = document.querySelectorAll('.sidebar button');
    sidebarButtons.forEach((button) => button.classList.remove('active'));

    // Show the selected tab
    const selectedTab = document.getElementById(tabId);
    if (selectedTab) {
        selectedTab.style.display = 'block';
    }

    // Highlight the active button
    const activeButton = Array.from(sidebarButtons).find((button) => button.textContent.trim().toLowerCase() === tabId.replace('_', ' '));
    if (activeButton) {
        activeButton.classList.add('active');
    }
}

// Show the default tab on page load
document.addEventListener('DOMContentLoaded', () => {
    showTab('ai_requests');
});

function addChatMessage(aiName, message) {
    const chatMessages = document.getElementById('chat-messages');

    // Create the response container
    const responseContainer = document.createElement('div');
    responseContainer.classList.add('response-container', `ai-${aiName.toLowerCase()}`);

    // Create the AI name header
    const aiHeader = document.createElement('h4');
    aiHeader.textContent = `${aiName}:`;
    responseContainer.appendChild(aiHeader);

    // Create the message content
    const messageContent = document.createElement('p');
    messageContent.classList.add('response-content');
    messageContent.textContent = message;
    responseContainer.appendChild(messageContent);

    // Create the TTS button
    const ttsButton = document.createElement('button');
    ttsButton.classList.add('tts-button');
    ttsButton.textContent = "🔊";
    ttsButton.onclick = () => generateAndPlayAudio(message);
    responseContainer.appendChild(ttsButton);

    // Append the response to the chat container
    chatMessages.appendChild(responseContainer);

    // Scroll to the bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendAIRequests() {
    const openAIToggle = document.getElementById('toggle-openai').checked;
    const googleAIToggle = document.getElementById('toggle-googleai').checked;
    const claudeAIToggle = document.getElementById('toggle-claudeai').checked; // Toggle for Claude AI
    const grokToggle = document.getElementById('toggle-grok').checked
    const userInput = document.getElementById('ai-input').value;

    if (!userInput.trim()) return;

    if (openAIToggle) {
        try {
            const response = await fetch('/api/openai_request', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ input: userInput }),
            });
            const result = await response.json();
            addChatMessage('OpenAI', result.reply || 'No response received.');
        } catch (error) {
            addChatMessage('OpenAI', `Error: ${error.message}`);
        }
    }

    if (googleAIToggle) {
        try {
            const response = await fetch('/api/googleai_request', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ input: userInput }),
            });
            const result = await response.json();
            addChatMessage('GoogleAI', result.reply || 'No response received.');
        } catch (error) {
            addChatMessage('GoogleAI', `Error: ${error.message}`);
        }
    }

    if (claudeAIToggle) {
        try {
            const response = await fetch('/api/claude_request', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ input: userInput }),
            });
            const result = await response.json();
            addChatMessage('ClaudeAI', result.reply || 'No response received.');
        } catch (error) {
            addChatMessage('ClaudeAI', `Error: ${error.message}`);
        }
    }

    if (grokToggle) {
        try {
            const response = await fetch('/api/grok_request', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ input: userInput }),
            });
            const result = await response.json();
            addChatMessage('Grok', result.reply || 'No response received.');
        } catch (error) {
            addChatMessage('Grok', `Error: ${error.message}`);
        }
    }
}

async function generateSDImage() {
    const prompt = document.getElementById('sd-prompt').value;
    const width = document.getElementById('sd-width').value || 512;
    const height = document.getElementById('sd-height').value || 512;

    if (!prompt.trim()) {
        alert("Please enter a prompt.");
        return;
    }

    const sdOutput = document.getElementById('sd-output');
    sdOutput.innerHTML = '<p>Generating image...</p>'; // Show loading indicator

    try {
        const response = await fetch('/api/stable_diffusion/txt2img', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt, width, height }),
        });
        const result = await response.json();

        if (result.generated_images) {
            sdOutput.innerHTML = ''; // Clear loading indicator
            result.generated_images.forEach(imgUrl => {
                const imgElement = document.createElement('img');
                imgElement.src = imgUrl;
                imgElement.alt = "Generated Image";
                sdOutput.appendChild(imgElement);
            });
        } else {
            sdOutput.innerHTML = '<p>No images generated.</p>';
        }
    } catch (error) {
        sdOutput.innerHTML = `<p>Error generating image: ${error.message}</p>`;
    }
}

async function sendTTSRequest() {
    const text = document.getElementById('tts-input').value;
    const voice = document.getElementById('voice-select').value;

    if (!text.trim()) {
        alert("Please enter text to synthesize.");
        return;
    }

    try {
        const response = await fetch('/api/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, voice }),
        });
        const result = await response.json();
        if (result.success) {
            alert("Audio synthesized successfully!");
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error("Error sending TTS request:", error);
    }
}

async function sendSTTRequest() {
    const audioFile = document.getElementById('audio-upload').files[0];
    if (!audioFile) {
        alert("Please upload an audio file.");
        return;
    }

    const formData = new FormData();
    formData.append('audio', audioFile);

    try {
        const response = await fetch('/api/stt', {
            method: 'POST',
            body: formData,
        });
        const result = await response.json();
        if (result.success) {
            document.getElementById('stt-result').innerText = result.transcription;
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error("Error sending STT request:", error);
    }
}

async function generateAndPlayAudio(text, voice = "en-US-AriaNeural") {
    if (!text.trim()) {
        alert("No text provided to generate audio.");
        return;
    }

    try {
        const response = await fetch('/api/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, voice }),
        });
        const result = await response.json();

        if (result.success) {
            const audioPlayer = document.getElementById('audio-player');
            audioPlayer.src = result.file_url;
            audioPlayer.play();
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error("Error generating audio:", error);
    }
}