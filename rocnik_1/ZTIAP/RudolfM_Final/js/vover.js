class Vover extends GameObject {
  constructor() {
    super();
    this.x = 450;
    this.y = 260;
    this.width = 230;
    this.height = 70;
    this.color = "red";
    this.text = "Vyhral si gratulujem"
    this.static = 1;
    this.physical = false;
  }

  move(game) {}

  draw(game) {
      game.context.font = "50pt Calibri"
      game.context.fillStyle = this.color
      game.context.fillText(this.text, 380, 100)
      game.context.font = "20pt Calibri"
      game.context.fillStyle = this.color
      game.context.fillText("Your score: " + game.score, 450, 400)
      game.context.fillText("Goal: 2520", 450, 450)
  }
}