let chatBox = document.getElementById('chat-box');

async function getAnswer(message) {
    const settings = {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prompt: message 
        })
    };
    //v632
    return fetch('/chatbot/response', settings)
            .then((response)=>response.text())
            .then((responseAnswer)=>{return responseAnswer});
}


async function sendMessage() {
  let messageInput = document.getElementById('message-input');
  let message = messageInput.value.trim();
  messageInput.value = '';

  if (message) {
    
    let messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add('me');
    messageElement.innerHTML = '<span class="name">Me:</span><div class="bubble">' + message + '</div>';
    chatBox.appendChild(messageElement);

    const result = await getAnswer(message);
      

    let responseElement = document.createElement('div');
    responseElement.classList.add('message');
    responseElement.classList.add('bot');
    responseElement.innerHTML = '<span class="name">Bot:</span><div class="bubble">' + result + '</div>';
    chatBox.appendChild(responseElement);

    scrollToBottom();
  }
}

function scrollToBottom() {
  chatBox.scrollTop = chatBox.scrollHeight;
}