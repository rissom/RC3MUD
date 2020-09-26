

var current_term_line = "";                  

var term = new window.Terminal.Terminal();
    term.open(document.getElementById('terminal'));
    term.write('Welcome to the \x1B[1;3;31mRC3MUD\x1B[0m!\r\n');
    term.focus();
    
    term.onData(e => {
  switch (e) {
    case '\r': // Enter
      if (current_term_line.length>0){
    	  ws.send( JSON.stringify( { "cmd": "user", "data": current_term_line  } ));
    	  current_term_line = "";
      }
    case '\u0003': // Ctrl+C
      prompt(term);
      break;
    case '\u007F': // Backspace (DEL)
      // Do not delete the prompt
      if (term._core.buffer.x > 2) {
        term.write('\b \b');
        current_term_line = current_term_line.slice(0,-1);
      }
    case '\t':
      possibleVerbs = actionList.filter ( y => y.startsWith( current_term_line ) );
      if ( possibleVerbs.length === 1 ){
        le = current_term_line.length;
        current_term_line = possibleVerbs[0] + " "; 
        term.write (current_term_line.slice(le));
      } else {
          term.write ( "\r\n"+possibleVerbs .join(" ") + "\n\r");
          term.write ( "$ " + current_term_line );
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

  if (msg.cmd=="html"){
    var wv = document.querySelector("#webview");
    wv.innerHTML = msg.data;
    // '<iframe src="http://unidaplan.com/rocket.html" width=250 height="250"</iframe>'
  }

  if (msg.cmd=="newcommandlist"){
    actionList = msg.data;
    console.log (actionList);
  }

  if (msg.cmd=="addcommandlist"){
    actionList = actionList.concat (msg.data);
    console.log (actionList);
  }
	
}

		