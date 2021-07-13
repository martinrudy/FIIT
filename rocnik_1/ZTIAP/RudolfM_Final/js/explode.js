class Explosion extends GameObject{
	constructor(){
		super();
	    this.image = document.getElementById("explode");
	    this.x = 0;
	    this.y = 0;
    	this.width = 140;
    	this.height = 140;
    	this.static = 1;
    	this.physical = false;
	}


	draw(){
		game.context.drawImage(this.image, this.x, this.y, this.width, this.height)
	}

}