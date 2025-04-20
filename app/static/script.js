let conversationHistory = [];

async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    input.value = '';
    
    try {
        // Send message to backend
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_history: conversationHistory
            })
        });
        
        const data = await response.json();
        
        // Add agent response to chat
        addMessage(data.response, 'agent');
        
        // Update debug info
        updateDebugInfo(data.debug_info);
        
        // Update conversation history
        conversationHistory.push(
            { role: 'user', content: message },
            { role: 'assistant', content: data.response }
        );
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, there was an error processing your request.', 'agent');
    }
}

function addMessage(content, sender) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
    
    messageDiv.appendChild(messageContent);
    messagesDiv.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function updateDebugInfo(debugInfo) {
    const dbQueryDiv = document.getElementById('dbQuery');
    const agentProcessingDiv = document.getElementById('agentProcessing');
    
    if (debugInfo.database_query) {
        dbQueryDiv.textContent = JSON.stringify(debugInfo.database_query, null, 2);
    }
    
    if (debugInfo.agent_processing) {
        agentProcessingDiv.textContent = JSON.stringify(debugInfo.agent_processing, null, 2);
    }
}

// Handle Enter key in input
document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Quick action buttons
function suggestAction(action) {
    const input = document.getElementById('userInput');
    
    switch(action) {
        case 'product':
            input.value = "What products do you have available?";
            break;
        case 'order':
            input.value = "What's the status of my order?";
            break;
        case 'cancel':
            input.value = "I want to cancel my order";
            break;
        case 'place':
            input.value = "I want to place an order for a Smartphone X with cash on delivery to 123 Main St, Anytown, USA";
            break;
    }
    
    // Focus on input
    input.focus();
} 