class SoundIcon extends GameObject{
	constructor(){
		super();
	    this.imageon = document.getElementById("soundon");
	    this.imageof = document.getElementById("soundoff");
    	this.x = 20;
    	this.y = 710;
    	this.width = 50;
    	this.height = 50;
    	this.static = 1;
    	this.physical = false;
	}

	drawon(){
		game.context.drawImage(this.imageon, this.x, this.y, this.width, this.height)
	}

	drawoff(){
		game.context.drawImage(this.imageof, this.x, this.y, this.width, this.height)
	}
}