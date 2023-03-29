
const messageForm = document.querySelector('#message-form');
const messageInput = document.querySelector('#message-input');
const messageArea = document.querySelector('#message-area');
const clientAlias = "You";
const serverAlias = "Bot";
const clientImg = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" fill=\"#dc3545\" \
class=\"bi bi-sign-turn-slight-right\" viewBox=\"0 0 16 16\"><path d=\"M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm2-3a2 \
2 0 1 1-4 0 2 2 0 0 1 4 0Zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4Zm-1-.004c-.001-.246-.154-.986-.832-1.\
664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10Z\"/></svg>"
const botImg = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"18\" height=\"18\" fill=\"#17a2b8\" class=\"bi bi-robot\" \
viewBox=\"0 0 16 16\"><path d=\"M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5ZM3 8.062C3 \
6.76 4.235 5.765 5.53 5.886a26.58 26.58 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.933.933 0 0 \
1-.765.935c-.845.147-2.34.346-4.235.346-1.895 0-3.39-.2-4.235-.346A.933.933 0 0 1 3 9.219V8.062Zm4.542-.827a.25.25 \
0 0 0-.217.068l-.92.9a24.767 24.767 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.149 2.02.193a.25.25 0 0 \
0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25.286 25.286 0 0 0 1.922-.188.25.25 0 0 \
0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135Z\"/>\
<path d=\"M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 \
2 0 0 0 2-2v-1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2V1.866ZM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 \
0 1-1-1V7.5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5Z\"/></svg>"

function addMessage(origin, message) {
    const messageElement = document.createElement('div');
    var imageMarkup = "";
    
    if (origin === clientAlias){
        messageElement.className = 'sender row'
        imageMarkup = "<div style=\"width: 0.8%\" class=\"mr-1\">" + clientImg + "</div>"
    }else{
        messageElement.className = 'receiver row'
        imageMarkup = "<div style=\"width: 0.8%\" class=\"mr-1\">" + botImg + "</div>"
    }
    
    messageElement.innerHTML =  imageMarkup + "<div style=\"width: 80%\" class=\"col-md w-90\">" + marked.parse(message)  + "</div>";
    messageArea.appendChild(messageElement);
    messageArea.scrollTop = messageArea.scrollHeight;
}


document.addEventListener('DOMContentLoaded', () => {
    

    messageForm.addEventListener('submit', event => {
        event.preventDefault();
        const message = messageInput.value;
        if (message === '') {
            return;
        }
        // console.log('You: ' + message);
        addMessage(clientAlias, message);
        sendMessage(message);
        messageInput.value = '';
    });

    

    function sendMessage(message) {
        fetch('/send_message', {
            method: 'POST',
            body: JSON.stringify({
                message: message
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })

        .then(response => response.json())
        .then(data => {
            // console.log('AI: ' + data['role']);
            // console.log('AI: ' + data['content']);
            addMessage(serverAlias, data['content']);
        })
        .catch(error => console.error(error));
    }
});

window.addEventListener("load", () => {

    console.log("page is fully loaded");
    function loadHistory(message) {
        fetch('/history', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })

        .then(response => response.json())
        .then(data => {
            
            // console.log('AI: ' + data[0].content);
            
            for (var i = 0; i < data.length; i++) {
                // console.log('AI: ' + data[i].role);
                if (data[i].role === 'user') {
                    addMessage(clientAlias, data[i].content);
                }
                else if (data[i].role === 'system') {
                    console.log(data[i].content);
                }
                else{
                    addMessage(serverAlias, data[i].content);
                }
                
            }
        })
        .catch(error => console.error(error));
    }
    loadHistory();

    hljs.highlightAll();
});