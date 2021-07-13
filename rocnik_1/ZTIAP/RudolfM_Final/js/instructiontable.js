class Instructiontable extends GameObject {
  constructor() {
    super();
    this.image = document.getElementById("controls")
    this.physical = false;
  }

  move(game) {}

  draw(game) {
      game.context.drawImage(this.image, 280, 250);
  }
}