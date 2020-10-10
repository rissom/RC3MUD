
const roomeditor_template = `<h2>Edit Room : LCC.Lounge</h2>
			<b>Exits</b><br /> N : Main Hall 3<br /> <select>
				<option>NW</option>
				<option>W</option>
				<option>SW</option>
				<option>S</option>
				<option>SE</option>
				<option>E</option>
				<option>NE</option>
			</select> area: <select>
				<option>LC3</option>
				<option>FOG</option>
				<option>C-Base</option>
			</select> room: <select>
				<option>MainHall1</option>
				<option>MainHall2</option>
				<option>Borg</option>
				<option>Adam</option>
			</select>
			<button>+ Add Exit</button>

			<br /> <br /> <b>Description</b> <br /> EN: <br />
			<textarea id="description" name="room_description_en" rows="10"
				cols="50" v-model="description_en"></textarea>
			<br /> DE: <br />
			<textarea id="description" name="room_description_de" rows="10"
				cols="50" v-model="description_de"></textarea>
			<br /> <br /> <b>Capacity</b> <br /> <input type="number" min="-1"
				max="40000" name="capacity" id="capacity" placeholder="-1">
			<br /> <br /> <b>Webview</b> <br /> EN: <br />
			<textarea id="description" name="webview_en" rows="10" cols="50"
				placeholder="<img src='https://thorstenrissom.eu/nouveau-rabumms.jpg' width=400  />"></textarea>
			<br /> DE: <br />
			<textarea id="description" name="webview_de" rows="10" cols="50"
				placeholder="Du befindest dich in der Lounge."></textarea>
			<br /> <br />
			<button v-on:click="cancel_edit()">cancel</button><button v-on:click="save_room()">save</button>`;

const roomeditor_methods = {
	save_room() {
    	console.log("save_room");
    },
    
    cancel_edit() {
    	console.log("cancel_edit");
    	document.querySelector("#terminal").classList.remove("d-none");
  	  	//document.querySelector("#roomeditor").classList.add("d-none");
    	console.log("this: ",this);
    	window.roomeditor.unmount("#roomeditor")
    }
  }

			
