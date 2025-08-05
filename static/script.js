if (document.getElementById('chat-messages')) {
    const socket = io();

    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    const nameDisplay = document.getElementById('name-display');
    const roomDisplay = document.getElementById('room-display');

    const name = nameDisplay ? nameDisplay.textContent : 'Anonymous';
    const room = roomDisplay ? roomDisplay.textContent : 'General';

    messageForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const message = messageInput.value.trim();

        if (message) {
            const now = new Date();
            const timestamp = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

            socket.emit('message', {
                'name': name,
                'message': message,
                'room': room,
                'timestamp': timestamp
            });

            messageInput.value = '';
        }
    });

    socket.on('connect', function () {
        socket.emit('join', { 'name': name, 'room': room });
        console.log('Connected to Socket.IO!');
    });

    socket.on('status', function (data) {
        const statusElement = document.createElement('div');
        statusElement.classList.add('chat-message', data.type);
        statusElement.innerHTML = `<em>${data.msg}</em>`;
        chatMessages.appendChild(statusElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });

    socket.on('chat_message', function (data) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message');

        if (data.name === name) {
            messageElement.classList.add('my-message');
        } else {
            messageElement.classList.add('other-message');
        }

        messageElement.innerHTML = `
            <span class="message-timestamp">${data.timestamp}</span>
            <span class="message-name">${data.name}</span>: 
            <span class="message-text">${data.message}</span>
        `;

        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });

    window.addEventListener('beforeunload', function () {
        socket.emit("leave", { 'name': name, 'room': room });
    });
}
