class Cross extends GameObject {
  constructor() {
    super();
    this.x = 1000;
    this.y = 30;
    this.width = 170;
    this.height = 45;
    this.color = "red";
    this.static = 1;
  }

  move(game) {}

  draw(game) {
  	game.context.beginPath();

    game.context.moveTo(this.x - 10, this.y - 10);
    game.context.lineTo(this.x + 10, this.y + 10);

    game.context.moveTo(this.x + 10, this.y - 10);
    game.context.lineTo(this.x - 10, this.y + 10);
    game.context.stroke();
  }
}