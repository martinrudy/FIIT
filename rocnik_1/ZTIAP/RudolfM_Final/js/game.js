class Game {
  constructor(canvasName) {
    this.canvas = document.getElementById(canvasName);
    this.context = canvas.getContext("2d");
    this.score = 0;
    this.start = 0;
    this.startTime = 0;
    this.dt = 0;
    this.level = 0;
    this.bomb = 0;
    this.soundexplosion = new SoundExplosion("./sound/explosion.mp3");
    this.soundprofit = new SoundProfit("./sound/earn_money.mp3");
    this.soundrope = new SoundRope("./sound/lano.mp3");
    this.soundpull = new SoundPull("./sound/pulling.mp3");
    this.soundwin = new SoundWin("./sound/vyhra.wav");
    this.soundlose = new SoundLose("./sound/prehra.wav");

    // Model
    this.mouse = { x: 0, y: 0, pressed: false, selected: false}
    this.keys = [];
    this.players = [];
    this.scene = firstscene();
    this.lastscene = this.scene;
  }


  loop() {
    if(this.startTime){
      var now = Date.now();
      this.dt = (now - this.start) / 1000;
      //console.log(dt);
    }

    if((this.level == 1 && this.score == 2520) || (this.level == 2 && this.score == 2520) || (this.level == 3 && this.score == 2520)){
      player.time = Math.floor(this.dt);
      this.players.push(player);
      offset += 35;
      this.scene = goverscene();
      this.lastscene = this.scene;
      if(sound == 1){
        this.soundwin.play();
      }
      this.level = 0;
    }

    if((this.level == 1 && Math.floor(this.dt) == 120) || (this.level == 2 && Math.floor(this.dt) == 90) || (this.level == 3 && Math.floor(this.dt) == 60)){
      this.scene = goverscene();
      this.lastscene = this.scene;
      if(sound == 1){
        this.soundlose.play();
      }
    }

    // Just move all the objects
    for (var i in this.scene) {
      if(this.scene[i] instanceof Hook)
        this.scene[i].move(this);
    }

    // Render the scene
    //console.log(this.scene);
    for (i in this.scene) {
      if(this.scene[i] instanceof SoundIcon){
        if(sound == 0){
          this.scene[i].drawoff()
        }
        else{
          this.scene[i].drawon()
        }
      }
      else{
        this.scene[i].draw(this);
      }
      //this.scene[i].draw(this);
    }

    // Loop animation
    requestAnimationFrame( this.loop.bind(this) );
  }
}