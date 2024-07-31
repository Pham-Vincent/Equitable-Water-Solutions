let API_BASE_URL;

// DOM Elements
const chatbotToggler = document.querySelector(".chatbot-toggler"); // Button to toggle the chatbot
const closeBtn = document.querySelector(".close-btn"); // Button to close the chatbot
const chatbox = document.querySelector(".chatbox"); // Chatbox container
const chatInput = document.querySelector(".chat-input textarea"); // Textarea for user input
const sendChatBtn = document.querySelector(".chat-input span"); // Button to send user message

// Variables
let userMessage = null; // Stores the user's message
const inputInitHeight = chatInput.scrollHeight; // Initial height of the input textarea
let eventSource = null; // Stores the EventSource object for server-sent events
let sessionId = null; // Stores the session ID for the chat

// Helper Functions
/**
 * Creates a new chat message element
 * @param {string} message - The message content.
 * @param {string} className - The class name for the message element (e.g. "incoming" or "outgoing").
 * @returns {HTMLElement} - The new chat message element.
 */
const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);

    // Determine content based on message type ("outgoing" or "incoming")
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").innerHTML = message;
    return chatLi;
}

/**
 * Displays an error message in the chatbox
 * @param {string} message - The error message to display.
 */
const showError = (message) => {
    const errorMessage = createChatLi(message, "incoming");
    chatbox.appendChild(errorMessage);

    // Scroll to the bottom of the chatbox to show the error message
    chatbox.scrollTo(0, chatbox.scrollHeight);
}

// Main Functions
/**
 * Initializes the chat with the FastAPI server hosted in an AWS EC2 instance.
 */
async function initializeChat() {
    try {        
        // Send a POST request to the server to initialize the chat session
        const initResponse = await fetch(`${API_BASE_URL}/initialize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_name: 'Salinity',
                database_name: 'main',
                session_id: '',
            }),
            credentials: 'include',
        });

        // Check if the response is OK
        if (!initResponse.ok) {
            throw new Error('Failed to initialize chat session');
        }

        // Parse the response as JSON
        const initData = await initResponse.json();

        // Store the session ID recieved by the server
        sessionId = initData.session_id;
        console.log('Initialized session ID:', initData.session_id);

    } catch (error) {
        // Display an error message if the chat initialization fails
        console.error('Error during chat initialization:', error);
        showError("Failed to initialize chat. Please try again later.");
    }
}

/**
 * Communicates with the FastAPI server to generate a response to the user's message. Actual LLM response generated on the server.
 * @param {HTMLElement} incomingChatLi - The chat message element for the incoming message.
 */
const generateResponse = async (incomingChatLi) => {
    const messageElement = incomingChatLi.querySelector("p");

    // Close the existing EventSource if it exists
    if (eventSource) {
        eventSource.close();
    }

    try {
        console.log('Creating new EventSource');
        const url = new URL(`${API_BASE_URL}/stream`);

        // Append the user's message and session ID to the URL
        url.searchParams.append('prompt', userMessage);
        url.searchParams.append('session_id', sessionId || '');
        
        // Create a new EventSource object to receive the server-sent events
        eventSource = new EventSource(url);

        eventSource.onmessage = (event) => {
            console.log('Received message:', event.data);

            // Replace the "Thinking..." message with the first chunk of the response
            if (messageElement.innerHTML === "Thinking...") {
                messageElement.innerHTML = event.data;
            } else {
                // Following the first chunk replacing "Thinking...", append subsequent chunks to the existing message
                messageElement.innerHTML += event.data;
            }

            // Scroll to the bottom of the chatbox to show the new message
            chatbox.scrollTo(0, chatbox.scrollHeight);
        };
        
        // Event listener for when the message stream is completed by the server
        eventSource.addEventListener("end-of-stream", () => {
            console.log("Message stream completed by server.")
            eventSource.close();
        })

        // Event listener for when the EventSource connection fails
        eventSource.onerror = (error) => {
            if (eventSource.readyState === EventSource.CLOSED) {
                console.log('EventSource closed normally.');
            } else {
                console.error('EventSource failed:', error);
                messageElement.innerHTML += "<br>Error: Couldn't complete the request.";
            }
            eventSource.close();
        };

        // Event listener for when the EventSource connection is opened
        eventSource.onopen = () => {
            console.log('EventSource connection opened');
        };
    } catch (error) {
        console.error('Error setting up EventSource:', error);
        messageElement.innerHTML += "<br>Error: Couldn't connect to the server.";
    }
}

/**
 * Handles the user's chat message and calls generate response to communicate with the server to get an LLM response.
 */
const handleChat = async () => {
    userMessage = chatInput.value.trim();
    if(!userMessage) return;

    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the user's message to the chatbox
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);

    // Display "Thinking..." message while waiting for the response
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    
    await generateResponse(incomingChatLi);
}

// Event Listeners
// Input textarea event listener
chatInput.addEventListener("input", () => {
    // Adjust the height of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

// Enter key event listener
chatInput.addEventListener("keydown", (e) => {
    // If Enter key is pressed without Shift key and the window
    // width is greater than 800px, handle the chat
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

// Send chat button event listener
sendChatBtn.addEventListener("click", handleChat);

// Close button event listener
closeBtn.addEventListener("click", () => {
    document.body.classList.remove("show-chatbot");
    if (eventSource) {
        eventSource.close();
    }
});

// Chatbot toggler event listener
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));

// Initialize the chat when the script loads
document.addEventListener('DOMContentLoaded', () => {
    fetch('/ApiKey')
        .then(response => response.json())
        .then(config => {
            API_BASE_URL = config.bot_url;
            initializeChat();
        })
        .catch(error => {
            console.error('Error fetching AI base URL:', error);
            showError("Failed to initialize chat. Please try again later. From chatbot.js, document.addEventListener('DOMContentLoaded', () => { ... });");
        })
});