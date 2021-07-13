class Gover extends GameObject {
  constructor() {
    super();
    this.x = 450;
    this.y = 260;
    this.width = 230;
    this.height = 70;
    this.color = "red";
    this.text = "Game Over"
    this.static = 1;
    this.physical = false;
  }

  move(game) {}

  draw(game) {
      game.context.font = "50pt Calibri"
      game.context.fillStyle = this.color
      game.context.fillText(this.text, 380, 100)
      game.context.beginPath();
      game.context.rect(440, 370, 230, 100);
      game.context.stroke();
      game.context.font = "20pt Calibri"
      game.context.fillStyle = this.color
      game.context.fillText("Your score: " + game.score, 450, 400)
      game.context.fillText("Goal: 2520", 450, 450)
  }
}