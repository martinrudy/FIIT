class Bomb extends GameObject {
  constructor(x, y, size) {
  	super(x, y, size);
    this.image = document.getElementById("bomb")
    this.width = 140
    this.height = 111
    this.static = 0
  }

  move(game) {}

  draw(game) {
    game.context.drawImage(this.image, this.x, this.y);
  }
}