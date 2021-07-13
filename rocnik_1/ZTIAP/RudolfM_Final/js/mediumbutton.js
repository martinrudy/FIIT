class Mediumbutton extends GameObject {
  constructor() {
    super(415, 350, 120);
    this.width = 220;
    this.height = 45;
    this.color = "red";
    this.static = 1;
    this.physical = false;
  }

  move(game) {}

  draw(game) {
    game.context.beginPath();
    game.context.rect(410, 320, 230, 45);
    game.context.stroke();
    game.context.font = "30pt Calibri"
    game.context.fillStyle = this.color
    game.context.fillText("Medium level", this.x, this.y)
  }
}