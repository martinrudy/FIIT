var game;
var time;
var music;
var sound;
var player;
var offset = 20;

// Just start up our game
window.onload = function () {
  game = new Game("canvas");
  game.canvas.onclick = mouseClick;
  game.loop();
  music = new Sound("./sound/menu_song.mp3");
  sound = 0;
};

function mouseClick(event) {
    var x = event.pageX - game.canvas.offsetLeft
    var y = event.pageY - game.canvas.offsetTop


    for(var i in game.scene) {
      var object = game.scene[i]
      if(x > object.x && x < object.x + object.width &&
        (y + 20)> object.y && (y + 20) < object.y + object.height) {
          if(object instanceof Play){
            player = new Player(offset);
            game.scene = levelsscene();
            game.lastscene = game.scene;
          }
          if(object instanceof Easybutton){
          	game.score = 0;
            game.startTime = 1;
            game.level = 1;
            game.scene = easy();
            game.lastscene = game.scene;
            game.start = Date.now();
            //console.log(game.lastscene);
          }
          if(object instanceof Mediumbutton){
            game.score = 0;
          	game.startTime = 1;
            game.level = 2;
            game.scene = medium();
            game.lastscene = game.scene;
            game.start = Date.now();
            //console.log(game.lastscene);
          }
          if(object instanceof Hardbutton){
            game.score = 0;
          	game.startTime = 1;
            game.level = 3;
            game.scene = hard();
            game.lastscene = game.scene;
            game.start = Date.now();
            //console.log(game.lastscene);
          }
          if(object instanceof Instructions){
            game.scene = instructionscene();
          }
          if(object instanceof Cross){
          	//console.log("blabla");
          	game.scene = game.lastscene;
          }
          if(object instanceof Title){
            game.lastscene = game.scene;
            game.scene = firstscene();
          }

          if(object instanceof Playagain){
            game.scene = firstscene();
            game.lastscene = game.scene;
          }
          if(object instanceof ScoreBoard){
            console.log("hakunamatata");
            game.scene = tablescene();
          }
          if(object instanceof SoundIcon){
            if(sound == 0){
              sound = 1
              music.play()
            }
            else{
              sound = 0
              music.stop()
            }
          }
      }
    }
}

window.onkeydown = function(event) {
  game.keys[event.keyCode] = true;
  //console.log(game.keys);
  for(var i in game.scene) {
      var object = game.scene[i]
      if(object instanceof Hook){
      	object.onkeyDown();
      }
  }
};

window.onkeyup = function(event) {
  game.keys[event.keyCode] = false;
  //console.log(game.keys);
};

