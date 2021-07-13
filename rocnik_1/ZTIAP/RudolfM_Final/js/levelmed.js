medium = function() {
  return [
      new Background(),
      new Miner(),
      new Hook(),
      new Rope(),
      new Instructions(),
      new Title(),
      new Gold(600, 380, 120),
      new Gold(150, 300, 120),
      new SmallGold(370, 200, 60),
      new SmallGold(350, 370, 60),
      new Mysterybox(450, 280, 120),
      new Mysterybox(80, 500, 120),
      new Bomb(30, 600, 120),
      new Bomb(700, 600, 120),
      new BigCoal(300, 550, 90),
      new BigCoal(750, 300, 90),
      new Diamond(250, 700, 60),
      new Diamond(550, 600, 60),
      new Diamond(890, 550, 60),
      new SoundIcon(),
      new Score("/2520"),
      new Time("/90")
  ];
};