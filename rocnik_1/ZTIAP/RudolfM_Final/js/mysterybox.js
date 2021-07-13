class Mysterybox extends GameObject {
  constructor(x, y, size) {
  	super(x, y, size);
    this.image = document.getElementById("mysterybox");
    this.width = 140;
    this.height = 111;
    this.size = 120;
    this.physical = true;
  }

  move(game) {}

  draw(game) {
    game.context.drawImage(this.image, this.x, this.y);
  }

  showbonus(){
    var x = Math.floor((Math.random() * 3) + 1);
    if(x == 1){
      time = 3;
    }
    else if(x == 2){
      for(var i in game.scene) {
        var object = game.scene[i]
        if(object instanceof Hook){
          object.speed = object.speed * 2;
          object.angleSpeed = 3;
        }
      }

    }
    else if(x == 3){
      game.scene.push(new Dinamite())
      game.bomb = 1;
    }
  }
}