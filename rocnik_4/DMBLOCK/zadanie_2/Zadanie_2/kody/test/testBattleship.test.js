const Battleship = artifacts.require("Battleship");

contract("Battleship", (accounts) => {
  let battleship;
  let expectedGame;

  before(async () => {
      battleship = await Battleship.deployed();
  });

  describe("Check if game over", async () => {
    it("check if game is over", async () => {
        const resultGame = await battleship.is_game_over({from: accounts[0]});
        expectedGame = false;
        assert.equal(resultGame, expectedGame, "At the beginning can not be over");
    });

    it("Check addresses both players", async () => {
        const players = await battleship.get_players({from: accounts[0]});
        
          
        assert.equal(players['0'], '0x0000000000000000000000000000000000000000', "The address of the player1 should be address(0) when bids was not set.");
        assert.equal(players['1'], '0x0000000000000000000000000000000000000000', "The address of the player2 should be address(0) when bids was not set.");
    });

    it("check one ship if is valid", async () => {
        await battleship.check_one_ship("0x7472756532303532333331333034", [], 0, accounts[1], {from: accounts[0]});
        const result = await battleship.get_checked_ship({from: accounts[0]})
        
          
        assert.equal(result, false, "Passed ship should not be valid");
    });

    it("should get count of proved ships", async () => {
        await battleship.check_one_ship("0x7472756532303532333331333034", [], 0, accounts[0], {from: accounts[0]});
        const count = await battleship.get_ships_count({from: accounts[0]});
          
        assert.equal(BigInt(count), BigInt(0), "Proved ships should be 0 if the game have not start yet");
    });

    it("Store a bid", async () => {
        await battleship.store_bid({from: accounts[0], value: 1*10**18});
        const bid = await battleship.get_player_bid({from: accounts[0]});
        assert.equal(BigInt(bid), BigInt(1*10**18), "Proved ships should be 0 if the game have not start yet");
    });
  });

});