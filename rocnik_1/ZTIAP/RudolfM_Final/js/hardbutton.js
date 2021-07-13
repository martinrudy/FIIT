class Hardbutton extends GameObject {
  constructor() {
    super(450, 420, 120);
    this.width = 170;
    this.height = 45;
    this.color = "red";
    this.static = 1;
    this.physical = false;
  }

  move(game) {}

  draw(game) {
    game.context.beginPath();
    game.context.rect(445, 390, 170, 45);
    game.context.stroke();
    game.context.font = "30pt Calibri"
    game.context.fillStyle = this.color
    game.context.fillText("Hard level", this.x, this.y)
  }
}