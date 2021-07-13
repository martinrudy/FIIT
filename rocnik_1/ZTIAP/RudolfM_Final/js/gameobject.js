class GameObject {
  constructor(x, y, size) {
    // Constructor, generates a new GameObject
    this.x = x;
    this.y = y;
    this.size = size;
    this.physical = true;
  }

  move(game) {}

  // Check object collision
  checkCollision(scene) {
    // Test collision
    for (var i in scene) {
      var obj = scene[i];
      // Object is not physical
      if (obj == this || !obj.physical) continue;
      var test =
        this.x >= obj.x + obj.size ||
        this.x + this.size <= obj.x ||
        this.y >= obj.y + obj.size ||
        this.y + this.size <= obj.y;
      if (!test) {
        return obj;
      }
    }
    return false;
  }

  // Draw self
  draw(game) {
    var ctx = game.context;
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.fillStyle = "red";
    ctx.fillRect(0, 0, this.size, this.size);
    ctx.restore();
  }
}