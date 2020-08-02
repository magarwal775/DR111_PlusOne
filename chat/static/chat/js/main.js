$("#profile-img").click(function () {
    $("#status-options").toggleClass("active");
});

$(".expand-button").click(function () {
    $("#profile").toggleClass("expanded");
    $("#contacts").toggleClass("expanded");
});


function scroll_up() {
    $('.messages').animate({ scrollTop: 0 }, 'fast');
}

$('.submit').click(function () {
    scroll();
});

$('#check_older_messages').click(function () {
    scroll_up();
});

var new_uri = window.location.protocol === 'https://' ? 'wss://' : 'ws://';
const chatSocket = new ReconnectingWebSocket(
    new_uri + window.location.host +
    '/ws/chat/' + roomName + '/');

chatSocket.onopen = function (e) {
    fetchMessages(true);
}

chatSocket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    console.log(data);
    if (data['command'] === 'messages') {
        for (let i = 0; i < data['messages'].length; i++) {
            createMessage(data['messages'][i]);
        }
    } else if (data['command'] === 'new_message') {
        createMessage(data['message']['message']);
        scroll();
    }
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if (message !== "") {
        chatSocket.send(JSON.stringify({
            'message': message,
            'from': username,
            'command': 'new_message',
            'roomName': roomName
        }));
        messageInputDom.value = '';
    }
};

function fetchMessages(recent) {
    chatSocket.send(JSON.stringify({ 'command': 'fetch_messages', 'roomName': roomName }));
}

function convertToMonth(index) {
    switch (index) {
        case 1:
            return 'Jan'
        case 2:
            return 'Feb'
        case 3:
            return 'Mar'
        case 4:
            return 'Apr'
        case 5:
            return 'May'
        case 6:
            return 'Jun'
        case 7:
            return 'Jul'
        case 8:
            return 'Aug'
        case 9:
            return 'Sep'
        case 10:
            return 'Oct'
        case 11:
            return 'Nov'
        case 12:
            return 'Dec'
    }
}

function formatDate(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;

    return date.getDate() + " " + convertToMonth(date.getMonth() + 1) + "  " + strTime;
}

function createMessage(data) {
    var author = data['author'];
    var dateTag = document.createElement('p');
    var imgTag = document.createElement('img');
    var body = document.createElement('div');
    var headerTag = document.createElement('div');
    var nameTag = document.createElement('strong')
    var msgTag = document.createElement('p');
    var contain = document.createElement('div');
    var boxTag = document.createElement('div');

    var date_posted = new Date(data.timestamp);

    nameTag.className = 'small text-muted';
    nameTag.textContent = author;

    msgTag.textContent = data.content;

    dateTag.textContent = formatDate(date_posted);

    headerTag.className = 'header';

    if (!(author === first_name)) {
        contain.className = "media w-25 mb-3";
        contain.appendChild(imgTag);
        imgTag.src = data["author_profile_img"];
        imgTag.width = "50";
        imgTag.className = "rounded-circle";
        body.className = "media-body ml-3";
        contain.appendChild(body);
        body.appendChild(nameTag);
        body.appendChild(boxTag);
        boxTag.className = "bg-light rounded py-2 px-3 mb-2";
        msgTag.className = "text-small mb-0 text-muted";
        msgTag.style = "overflow-wrap: break-word; max-width: 20em";
        boxTag.appendChild(msgTag);
        body.appendChild(dateTag);
        dateTag.className = "small text-muted";
    } else {
        contain.className = "media w-25 ml-auto mb-3";
        contain.appendChild(body);
        body.className = "media-body";
        body.appendChild(boxTag);
        boxTag.className = "bg-primary rounded py-2 px-3 mb-2";
        boxTag.appendChild(msgTag);
        msgTag.className = "text-small mb-0 text-white";
        msgTag.style = "overflow-wrap: break-word; max-width: 20em";
        body.appendChild(dateTag);
        dateTag.className = "small text-muted";
    }
    document.querySelector('#chat-log').appendChild(contain);
    var d = $('#chat-log');
    d.scrollTop(d.prop("scrollHeight"));
}