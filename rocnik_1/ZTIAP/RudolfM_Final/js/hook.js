class Hook extends GameObject {
  constructor() {
  	super();
    this.image = document.getElementById("hook");
    this.x = 510;
    this.y = 120;
    this.dy = 5;
    this.width = 41;
    this.height = 48;
    this.angle = -0.5;
    this.mine = 0;
    this.size = 12;
    this.angleSpeed = 1;
    this.speed = 5;
    this.trigger;
    this.kolizia;
    this.switch = 0;
    this.physical = false;
    this.last = 0;
  }

  move(game) {
  	if(this.mine == 1){
      time = 2
      var last_x = this.x;
      var last_y = this.y;

      if(game.bomb == 3 && (this.last - 30) >= this.y){
          for(var i in game.scene) {
            var object = game.scene[i]
            if(object instanceof Explosion){
              object.x = -999;
              object.y = -999;
            }
          }
      }

      if(game.bomb == 2){
        this.kolizia.x = -999;
        this.kolizia.y = -999;
        if(this.kolizia instanceof Gold){
          game.score += 200;
        }
        if(this.kolizia instanceof SmallGold){
          game.score += 100;
        }
        if(this.kolizia instanceof Diamond){
          game.score += 600;
        }
        if(this.kolizia instanceof BigCoal){
          game.score += 60;
        }
        if(this.kolizia instanceof SmallCoal){
          game.score += 20;
        }
        if(this.kolizia instanceof Mysterybox){
            this.kolizia.showbonus();
        }
        this.trigger = 0;
        game.bomb = 3;
        this.speed = this.speed * 2;
      }

      if (this.switch == 1 && this.kolizia){
        console.log(this.kolizia);
        this.speed = this.speed * 0.5;
        this.switch = 0
      }

      if (!this.checkCollision(game.scene) && this.trigger == 1) {
        var uhol = this.angle + 40 * Math.PI / 180

        if(sound == 1){
          game.soundrope.play();
        }

        this.x = this.x + Math.cos(uhol) * this.speed;
        this.y = this.y + Math.sin(uhol) * this.speed;
        if(this.x  >= game.canvas.width || this.y >= game.canvas.height || this.x <= 0 || this.y <= 0){
          this.trigger = 0;
        }
      }


      if(this.kolizia = this.checkCollision(game.scene) && this.trigger == 1){
        this.trigger = 0;
        this.switch = 1;
        for(var i in game.scene) {
          var object = game.scene[i]
          if(object instanceof Explosion){
            object.x = this.kolizia.x;
            object.y = this.kolizia.y;
          }
        }
      }
      if(this.kolizia = this.checkCollision(game.scene)){
        this.x = last_x;
        this.y = last_y;
      }
      if (this.trigger == 0) {
        var uhol = this.angle + 40 * Math.PI / 180
        this.x -= Math.cos(uhol) * this.speed;
        this.y -= Math.sin(uhol) * this.speed;

        if(this.kolizia instanceof Gold || this.kolizia instanceof Mysterybox ||
          this.kolizia instanceof SmallGold || this.kolizia instanceof Diamond ||
          this.kolizia instanceof BigCoal || this.kolizia instanceof SmallCoal){

          this.kolizia.x = last_x - 10;
          this.kolizia.y = last_y - 10;

          if(sound == 1){
            game.soundpull.play();
          }

          if(this.y <= 120){
            if(this.kolizia instanceof Gold){
              game.score += 200;
            }
            if(this.kolizia instanceof SmallGold){
              game.score += 100;
            }
            if(this.kolizia instanceof Diamond){
              game.score += 600;
            }
            if(this.kolizia instanceof BigCoal){
              game.score += 60;
            }
            if(this.kolizia instanceof SmallCoal){
              game.score += 20;
            }
            this.speed = this.speed * 2;
            this.kolizia.x = -999;
            this.kolizia.y = -999;
            if(sound == 1){
              game.soundprofit.play();
            }
            //this.speed = this.speed * 2;
            /*if(this.kolizia instanceof Mysterybox){
            this.kolizia.showbonus();
            this.kolizia.x = -999;
            this.kolizia.y = -999;
            }
            else{
              this.kolizia.x = -999;
              this.kolizia.y = -999;
            }*/
          }
        }
        if(this.kolizia instanceof Bomb){
          //console.log("blubli");
          game.soundlose.play();
          game.scene = goverscene();
          game.lastscene = game.scene;
        }

        if(this.y <= 120){
          time = 0;
          this.mine = 0;
          if(this.kolizia instanceof Mysterybox){
            this.kolizia.showbonus();
            this.kolizia.x = -999;
            this.kolizia.y = -999;
          }
          /*else if(!(this.kolizia instanceof Dinamite)){
            this.kolizia.x = -999;
            this.kolizia.y = -999;
          }*/
        }

      }


    }
  }

  draw() {
    console.log(game.bomb);

    if(time != 3){
      if(this.angle <= -0.5){
        time = 0
      }
      if(this.angle >= 2){
        time = 1
      }

      if(time == 0){
        this.angle += this.angleSpeed * Math.PI / 180;
      }
      else if(time == 1){
        this.angle -= this.angleSpeed * Math.PI / 180;
      }
    }
	  game.context.save()
   	game.context.translate(this.x, this.y);
   	game.context.rotate(this.angle);
   	game.context.drawImage(this.image, this.width / -4, this.height / -4, this.height, this.width)
    game.context.restore()
  }


  onkeyDown(){
    if (game.keys[40]){
      this.mine = 1
      this.trigger = 1
    }
    if (game.keys[38] && game.bomb == 1 && this.mine == 1){

      if(sound == 1){
        game.soundexplosion.play();
      }

    for(var i in game.scene) {
      var object = game.scene[i]
      if(object instanceof Dinamite){
        object.x = -999;
        object.y = -999;
      }
    }

      game.scene.push(new Explosion())
      for(var i in game.scene) {
        var object = game.scene[i]
        if(object instanceof Explosion){
          object.x = this.x;
          object.y = this.y;
          this.last = this.y;
          game.bomb = 2;
        }
      }
    }
  }



}
