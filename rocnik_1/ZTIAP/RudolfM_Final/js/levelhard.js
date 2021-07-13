hard = function() {
  return [
      new Background(),
      new Miner(),
      new Hook(),
      new Rope(),
      new Instructions(),
      new Title(),
      new Gold(680, 420, 120),
      new Gold(100, 300, 120),
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
      new SmallCoal(500, 450, 60),
      new SmallCoal(630, 300, 60),
      new SmallCoal(250, 300, 60),
      new SoundIcon(),
      new Score("/2520"),
      new Time("/60")
  ];
};