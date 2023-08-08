// JavaScript code to handle the chat functionality
document.getElementById("sendBtn").addEventListener("click", function () {
    var userInput = document.getElementById("userInput").value;

    // Clear the input field
    document.getElementById("userInput").value = "";

    // Add user's message to the chat box with appropriate classes
    var chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += '<p class="chat-message user-message">You: ' + userInput + '</p>';

    // Make an AJAX POST request to the Flask route to get the bot's response
    var api_key = "enter apikey";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/chat", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("API-Key", api_key); // Replace with the actual API key
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText).response;
                // Add bot's response to the chat box with appropriate classes
                chatbox.innerHTML += '<p class="chat-message bot-message">Bot: ' + response + '</p>';
            } else {
                var error = JSON.parse(xhr.responseText).error;
                // Handle the error, if necessary
                console.error("Error:", error);
            }
        }
    };
    xhr.send(JSON.stringify({ message: userInput }));
});


// Add an event listener for the "Enter" key on the input box
document.getElementById('userInput').addEventListener('keypress', function(event) {
    // Check if the Enter key is pressed (keyCode 13)
    if (event.keyCode === 13) {
        // Trigger a click event on the "Send" button
        document.getElementById('sendBtn').click();
    }
});