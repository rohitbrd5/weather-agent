document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chat-form"); // This form no longer exists, but the input elements are still relevant.
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const micButton = document.getElementById("mic-button");
  const sendButton = document.getElementById("send-button");
  const voiceStatus = document.getElementById("voice-status");
  const inputArea = document.querySelector(".input-area");

  let isListening = false;
  let recognition;
  let synth = window.speechSynthesis;
  let conversationHistory = []; // Initialize conversation history

  // Check for Speech Recognition API support
  if ("webkitSpeechRecognition" in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
      isListening = true;
      micButton.classList.add("listening");
      voiceStatus.textContent = "Listening...";
      userInput.focus();
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      userInput.value = transcript;
      if (transcript.trim() !== "") {
        sendMessage(transcript);
      }
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error", event);
      voiceStatus.textContent = "Error listening. Try again.";
      isListening = false;
      micButton.classList.remove("listening");
    };

    recognition.onend = () => {
      isListening = false;
      micButton.classList.remove("listening");
      voiceStatus.textContent = "Tap mic to speak";
    };
  } else {
    micButton.style.display = "none";
    voiceStatus.textContent = "Speech recognition not supported.";
    console.warn(
      "Web Speech API (Speech Recognition) not supported in this browser."
    );
  }

  // Speech Synthesis (Text-to-Speech) function
  const speak = (text) => {
    if (synth.speaking) {
      synth.cancel();
    }
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    utterance.onstart = () => {
      micButton.disabled = true; // Disable mic while bot is speaking
      sendButton.disabled = true;
      userInput.disabled = true;
      inputArea.classList.add("speaking");
    };
    utterance.onend = () => {
      micButton.disabled = false;
      sendButton.disabled = false;
      userInput.disabled = false;
      inputArea.classList.remove("speaking");
      userInput.focus(); // Focus input after bot speaks
    };
    utterance.onerror = (event) => {
      console.error("Speech synthesis error", event);
      micButton.disabled = false;
      sendButton.disabled = false;
      userInput.disabled = false;
      inputArea.classList.remove("speaking");
    };
    synth.speak(utterance);
  };

  const appendMessage = (sender, text) => {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    const bubbleDiv = document.createElement("div");
    bubbleDiv.classList.add("message-bubble");
    bubbleDiv.innerHTML = text; // Use innerHTML to render HTML
    messageDiv.appendChild(bubbleDiv);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Update conversation history
    conversationHistory.push({ type: sender === 'user' ? 'human' : 'ai', content: text });
  };

  // Function to apply formatting (e.g., bold from markdown)
  const formatMessageText = (text) => {
      // Replace **text** with <strong>text</strong>
      return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  };

  const sendMessage = async (query) => {
    if (query) {
      appendMessage("user", query);
      userInput.value = "";

      try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ user_query: query, history: conversationHistory }), // Pass history
        });
        const data = await response.json();
        appendMessage("agent", formatMessageText(data.response)); // Apply formatting here
        speak(data.response); // Speak the raw response without tags
      } catch (error) {
        console.error("Error:", error);
        const errorMessage = "Sorry, something went wrong.";
        appendMessage("agent", errorMessage);
        speak(errorMessage);
      }
    }
  };

  // Event Listeners
  sendButton.addEventListener("click", (e) => {
    e.preventDefault();
    const query = userInput.value.trim();
    sendMessage(query);
  });

  micButton.addEventListener("click", () => {
    if (synth.speaking) {
      synth.cancel(); // Stop speaking if mic is pressed during TTS
    }
    if (isListening) {
      recognition.stop();
    } else {
      recognition.start();
    }
  });

  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage(userInput.value.trim());
    }
  });
});
