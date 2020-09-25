

var current_term_line = "";

var term = new window.Terminal.Terminal();
    term.open(document.getElementById('terminal'));
    term.write('Hello from \x1B[1;3;31mxterm.js\x1B[0m $ ')
    
    term.onData(e => {
  switch (e) {
    case '\r': // Enter
    	ws.send( JSON.stringify( { "cmd": "user", "data": current_term_line  } ));
    	current_term_line = "";
    case '\u0003': // Ctrl+C
      prompt(term);
      break;
    case '\u007F': // Backspace (DEL)
      // Do not delete the prompt
      if (term._core.buffer.x > 2) {
        term.write('\b \b');
      }
      break;
    default: // Print all other characters for demo
      term.write(e);
    current_term_line = current_term_line+e;
  }
});
        
function prompt(term) {
	term.write('\r\n$ ');
}
        
        
var ws = new WebSocket("ws://"+window.location.host+"/websocket");

ws.onopen = function() {
	ws.send( JSON.stringify( { "cmd": "ping" } ));
};

ws.onerror = function() {
	console.log("ws onerror");
};

ws.onclose = function() {
	console.log("ws onclose");
};

var nextMessageIsBinary = false;
ws.onmessage = function (message) {
	console.log("ws: "+message.data);
	if (nextMessageIsBinary===false) {
		var msg = JSON.parse(message.data);
		if (msg.binary==true) {
			nextMessageIsBinary = msg;
			return;
		}
		if (msg.cmd=="text") {
			term.write(msg.data+'\r\n$ ');
		}
	} else {
		if (nextMessageIsBinary.cmd=="liveimage") {
			loadMessageIntoCanvas(message, nextMessageIsBinary, document.querySelector('#imageCanvas'),false);
			nextMessageIsBinary = false;
			if (doLiveUpdate) {
				requestImage(currentImageType);
			}
			return;
		}
	}
}

		