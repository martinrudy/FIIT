class Player{
	constructor(offset){
		this.name = "Player";
		this.time = 0;
		this.x = 450;
		this.y = 200 + offset;
	}

	draw(){
		game.context.font = "30pt Calibri";
      	game.context.fillStyle = this.color;
      	game.context.fillText(this.name, this.x, this.y);
      	game.context.fillText(this.time +  " sec", this.x + 180, this.y);
      	game.context.beginPath();
      	game.context.rect(440, 180, 270, 300);
      	game.context.stroke();
	}

}
