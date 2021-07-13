class Dinamite extends GameObject {
  constructor() {
  	super();
    this.image = document.getElementById("dinamite")
    this.x = 600;
    this.y = 5;
    this.width = 140
    this.height = 111
    this.size = 120
    this.static = 1
  }

  move(game) {}

  draw(game) {
    game.context.drawImage(this.image, this.x, this.y);
  }


}