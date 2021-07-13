class Score extends GameObject {
  constructor(text) {
    super();
    this.width = 600;
    this.height = 70;
    this.color = "red";
    this.static = 1;
    this.physical = false;
    this.text = text;
  }

  move(game) {}

  draw(game) {
    game.context.font = "20pt Calibri"
    game.context.fillStyle = this.color
    game.context.fillText("Score: " + game.score + this.text, 20, 70)
  }
}