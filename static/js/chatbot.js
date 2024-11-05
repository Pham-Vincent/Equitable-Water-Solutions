/*
title: chatbot.js

Description: This file controls the chatbot functionality.

Authors: Spencer Presley

Date: 10/31/24
*/

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
        const initResponse = await fetch('/initialize-ai-chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: '',
            }),
        });

        // Check if the response is OK
        if (!initResponse.ok) {
            throw new Error('Failed to initialize chat session');
        }

        // Parse the response as JSON
        const initData = await initResponse.json();

        // Store the session ID recieved
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

    try {
        const response = await fetch('/ai-stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt: userMessage,
                session_id: sessionId || '',
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to generate response');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let isFirstChunk = true;

        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                break;
            }

            const chunk = decoder.decode(value);
            if (chunk === "end-of-stream") {
                break;
            } else if (messageElement.innerHTML === "Thinking...") {
                messageElement.innerHTML = chunk;
            } else {
                messageElement.innerHTML += chunk;
            }

            chatbox.scrollTo(0, chatbox.scrollHeight);
        }
    } catch (error) {
        console.error('Error during chat response generation:', error);
        showError("Failed to generate response. Please try again later.");
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
    initializeChat();
});