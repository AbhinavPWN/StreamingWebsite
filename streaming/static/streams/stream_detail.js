const socket = new WebSocket('wss://localhost:8000/ws/stream/7/');

socket.onopen = function(event) {
  console.log('WebSocket connection established');
};

socket.onmessage = function(event) {
  console.log('Websocket message received')
  const message = JSON.parse(event.data);
  // Handle the received streaming data, update the UI, or perform actions based on the data
  // For example, you can append the data to the stream container element
  const streamContainer = document.getElementById('stream-container');
  streamContainer.innerHTML += message;
};

socket.onclose = function(event) {
  console.log('WebSocket connection closed');
};
