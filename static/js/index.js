var socket = new WebSocket("ws://localhost:8000/ws");
function send_data () {
    el = document.getElementById('input_node');
    socket.send(el.value);
    el.value = "";
}
socket.onopen = function() {
    console.log("Connected");
};

socket.onclose = function(event) {
    if (event.wasClean) {
        alert('Clear exit');
    } else {
        alert('error connection'); // например, "убит" процесс сервера
    }
    alert('Code: ' + event.code + ' Event: ' + event.reason);
};

socket.onmessage = function(event) {
    ul = document.getElementById("test");
    li = document.createElement("li");
    li.innerText = event.data;
    ul.appendChild(li);
};

socket.onerror = function(error) {
    alert("Error " + error.message);
};
