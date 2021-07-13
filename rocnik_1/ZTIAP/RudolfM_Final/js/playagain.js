class Playagain extends GameObject {
  constructor() {
    super();
    this.x = 450;
    this.y = 260;
    this.width = 230;
    this.height = 50;
    this.color = "red";
    this.text = "Game Over";
    this.static = 1;
    this.physical = false;
  }

  move(game) {}

  draw(game) {
    game.context.beginPath();
    game.context.rect(445, 220, 190, 50);
    game.context.stroke();
    game.context.font = "30pt Calibri";
    game.context.fillStyle = this.color;
    game.context.fillText("Main menu", 450, 260);
  }
}