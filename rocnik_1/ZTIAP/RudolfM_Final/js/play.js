class Play extends GameObject {
  constructor() {
    super(445, 150, 0);
    this.width = 170;
    this.height = 45;
    this.color = "red";
    this.static = 1;
    this.physical = false;
  }

  move(game) {}

  draw(game) {
    game.context.beginPath();
    game.context.rect(445, 150, 170, 45);
    game.context.stroke();
    game.context.font = "30pt Calibri"
    game.context.fillStyle = this.color
    game.context.fillText("Play game", 450, 180)
  }
}