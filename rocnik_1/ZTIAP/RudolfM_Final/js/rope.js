class Rope extends GameObject {
  constructor() {
  	super();
    this.physical = false;
  }

  move(game) {}

  draw(game) {
    game.context.beginPath();
    game.context.moveTo(520, 116);
      for(var i in game.scene) {
      var object = game.scene[i]
      if(object instanceof Hook){
      	 game.context.lineTo(object.x + 2, object.y - 1);
      }
    }
    game.context.stroke();
  }
}