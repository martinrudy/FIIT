class Sound {

	constructor(src){
		this.sound = document.createElement("audio");
    	this.sound.src = src;
        this.sound.loop = true;
    	this.sound.setAttribute("preload", "auto");
    	this.sound.setAttribute("controls", "loop");
    	this.sound.style.display = "none";
    	document.body.appendChild(this.sound);
	}


	play(){
        this.sound.play();
    }
    stop(){
        this.sound.pause();
    }
}