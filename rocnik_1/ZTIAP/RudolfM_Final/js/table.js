class Table{
	constructor(){
		this.x = 450;
		this.y = 400;
		this.xx = 500;
		this.yy = 400;
		this.color = "red";
	}

	draw(){
		for(var i in game.players){
			var object = game.players[i];
			//console.log(object);
			object.draw();
		}
	}

}