class ScoreBoard extends GameObject {
  constructor() {
    super(450, 320, 0);
    this.width = 170;
    this.height = 45;
    this.color = "red";
    this.static = 1;
    this.physical = false;
  }

  move(game) {}

  draw(game) {
    game.context.beginPath();
    game.context.rect(445, 290, 200, 50);
    game.context.stroke();
    game.context.font = "30pt Calibri";
    game.context.fillStyle = this.color;
    game.context.fillText("Score board", 450, 320);
  }
}