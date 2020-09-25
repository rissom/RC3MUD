

var current_term_line = "";

var term = new window.Terminal.Terminal();
    term.open(document.getElementById('terminal'));
    term.write('Hello from \x1B[1;3;31mRC3MUD\x1B[0m $ ')
    
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
	term.write('\r\n\x1B[1;3;31mConnection lost...\x1B[0m');
};

ws.onmessage = function (message) {
	console.log("ws: "+message.data);
	
	var msg = JSON.parse(message.data);
	
	if (msg.cmd=="text") {
		term.write('\b\b');
		term.write(msg.data+'\r\n$ ');
	}
	
}

		