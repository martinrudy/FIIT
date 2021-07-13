class Title extends GameObject {
  constructor() {
    super();
    this.x = 10;
    this.y = 30;
    this.width = 190;
    this.height = 45;
    this.color = "red";
    this.static = 1;
    this.physical = false;
  }

  move(game) {}

  draw(game) {
    game.context.font = "30pt Calibri"
    game.context.fillStyle = this.color
    game.context.fillText("Gold Miner", 10, 35)
  }
}