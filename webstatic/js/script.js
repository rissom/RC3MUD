

var playername = new URLSearchParams(window.location.search).get("name");
if (playername==null) {
	window.location.href = '/index.html';
}

var current_term_line = "";        
var actionList = ["say","rename"];
var cHistory = [];
var tempTermline = "";
var historyIndex = 0;


var term = new window.Terminal.Terminal();
    term.open(document.getElementById('terminal'));
    term.write('Welcome to the \x1B[1;3;31mRC3MUD\x1B[0m!\r\n');
    term.focus();
    
    term.onData(e => {
      // determine the Unicode code (only detects the first code! Arrows have 3 codes)
      // var hex = e.codePointAt(0).toString(16);
      // var result = "\\u" + "0000".substring(0, 4 - hex.length) + hex +" " ;
      // term.write(result)
  switch (e) {
    case '\r': // Enter
      if (current_term_line.length>0){
    	  var data = JSON.stringify( { "cmd": "user", "data": current_term_line  } );
    	  console.log("ws: --> "+data);
    	  ws.send( data );
    	  prompt(term);
        if (!cHistory.includes(current_term_line)){
          cHistory.push (current_term_line);
          cHistory = cHistory.slice(-100);      // keep history limited to 100 entries
        }
        historyIndex = 0;
    	  current_term_line = "";
      }
      break;
    case '\u0003': // Ctrl+C
      prompt(term);
      current_term_line = "";
      break;
    case '\u007F': // Backspace (DEL)
      // Do not delete the prompt
      if (term._core.buffer.x > 2) {
        term.write('\b \b');
        current_term_line = current_term_line.slice(0,-1);
      }
      break;
    case '\u001B\u005B\u0041': // Arrow up
        // console.log ("historyIndex", historyIndex);
        // console.log ("History", cHistory);
        // console.log ("Historylength: "+cHistory.length)
        if (historyIndex == 0 && current_term_line.length>0) {
          tempTermline = current_term_line;
        }
        if (historyIndex < cHistory.length) {
          historyIndex++;
          clearLine(term);
          current_term_line = cHistory.slice( - historyIndex )[0];
          term.write(current_term_line);
        }
      break;
    case '\u001B\u005B\u0043': // right
        // do nothing at all
      break;
    case '\u001B\u005B\u0042':  // arrow down
        // console.log ("historyIndex", historyIndex);
        // console.log ("History", cHistory);
        // console.log ("Historylength: "+cHistory.length)
        clearLine(term);
        if (historyIndex>1) {
          historyIndex--;
          current_term_line = cHistory.slice( - historyIndex )[0];
          term.write(current_term_line);
        } else {
          current_term_line = tempTermline;
        }
      break;
    case '\u001B\u005B\u0044':
        // like backspace
        if (term._core.buffer.x > 2) {
        term.write('\b \b');
        // term._core.buffer.x = current_term_line.length;
      }
      break;
    case '\t':
      possibleVerbs = actionList.filter ( y => y.startsWith( current_term_line ) );
      if ( possibleVerbs.length === 1 ){
        le = current_term_line.length;
        current_term_line = possibleVerbs[0] + " "; 
        term.write (current_term_line.slice(le));
      } else {
          let startsWith = possibleVerbs.reduce( (x,y) => { 
            let i=0;
            for (i=0; i < Math.min( x.length, y.length ) && x[i]==y[i]; i++){}
            return x.slice(0,i);
          })
          term.write ( "\r\n"+possibleVerbs .join(" ") + "\n\r");
          prompt(term)
          term.write ( startsWith );
          current_term_line = startsWith;
      }
      break;
    default: // Print all other characters for demo
      term.write(e);
    current_term_line = current_term_line+e;
  }
});


function prompt(term) {
	term.write('\r\n# ');
}


function clearLine(term){
  for (let i=0; i<current_term_line.length; i++){
    term.write('\b \b');
  } 
}
        
        
var ws = new WebSocket("ws://"+window.location.host+"/websocket");

ws.onopen = function() {
	ws.send( JSON.stringify( { "cmd": "ping" } ));
	ws.send( JSON.stringify( { "cmd": "user", "data": "rename "+playername } ));
};

ws.onerror = function() {
	console.log("ws onerror");
	
};

ws.onclose = function() {
	console.log("ws onclose");
	term.write('\r\n\x1B[1;3;31mConnection lost...\x1B[0m');
};

ws.onmessage = function (message) {
	console.log("ws: <-- "+message.data);
	
	console.log("ctl: "+current_term_line+" len: "+current_term_line.length);
	var msg = JSON.parse(message.data);
	
	if (msg.cmd=="text") {
		for (var i=0;i<current_term_line.length+2;i++) {
			term.write('\b \b');
		}
		term.write(msg.data+'\r\n$ ');
		term.write(current_term_line);
	}

  if (msg.cmd=="html"){
    var wv = document.querySelector("#webview");
    wv.innerHTML = msg.data;
    // '<iframe src="http://unidaplan.com/rocket.html" width=250 height="250"</iframe>'
  }
  if (msg.cmd=="video"){
	    var wv = document.querySelector("#videoview");
	    if (msg.enabled) {
	    	wv.classList.remove("d-none");
	    } else {
	    	wv.classList.add("d-none");
	    }
	    wv.innerHTML = msg.data;
	  }

  if (msg.cmd=="newcommandlist"){
    actionList = msg.data;
  }

  if (msg.cmd=="addcommandlist"){
    actionList = actionList.concat (msg.data);
  }

  if (msg.cmd=="removecommandlist"){
    // filter out everything that is included in the remove list: Not yet tested!
    newActionList = actionList.filter ( a =>  !msg.data.includes(a));  
  }
	
}

		