playscene = function() {
  return [
      new Background(),
      new Miner(),
      new Hook(),
      new Rope(),
      new Gold(450, 350, 120),
      new Instructions(),
      new Title(),
      new Mysterybox(450, 500, 120),
      new Bomb(550, 500, 120),
      new SoundIcon(),
      new Score(),
      new Time(),
      new SmallGold(10, 500, 60),
      new Diamond(450, 200, 60),
      new BigCoal(600, 170, 120),
      new SmallCoal(650, 250, 60)
  ];
};