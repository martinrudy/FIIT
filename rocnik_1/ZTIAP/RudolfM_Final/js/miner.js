class Miner extends GameObject {
  constructor() {
  	super();
    this.image = document.getElementById("miner");
    this.physical = false;
  }

  move(game) {}

  draw(game) {
    game.context.drawImage(this.image, 450, 10);
  }
}