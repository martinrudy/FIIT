class Instructions extends GameObject {
  constructor() {
    super();
    this.x = 750;
    this.y = 30;
    this.width = 170;
    this.height = 45;
    this.color = "red";
    this.static = 1;
    this.physical = false;
  }

  move(game) {}

  draw(game) {
      game.context.font = "30pt Calibri"
      game.context.fillStyle = this.color
      game.context.fillText("Instruction", 750, 30)
  }

}