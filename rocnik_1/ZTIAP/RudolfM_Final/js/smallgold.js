class SmallGold extends GameObject {
  constructor(x, y, size) {
  	super(x, y, size);
    this.image = document.getElementById("smallgold");
    this.width = 140
    this.height = 111
    this.physical = true;
  }

  move(game) {}

  draw(game) {
    game.context.drawImage(this.image, this.x, this.y);
  }
}