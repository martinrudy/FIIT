class Background extends GameObject {
  constructor() {
  	super();
    this.image = document.getElementById("image");
    this.physical = false;
  }

  move(game) {}

  draw(game) {
    game.context.drawImage(this.image, 0, 0);
  }
}