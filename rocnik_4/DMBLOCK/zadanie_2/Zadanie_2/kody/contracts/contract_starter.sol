pragma solidity >=0.4.22 <0.7.0;

//import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v3.0.0/contracts/cryptography/ECDSA.sol";
import "@openzeppelin/contracts/cryptography/ECDSA.sol";

contract Battleship {
    using ECDSA for bytes32;
    uint32 constant BOARD_LEN = 6;
    // Declare state variables here.
    // Consider keeping state for:
    // - player addresses
    // - whether the game is over
    // - board commitments
    // - whether a player has proven 10 winning moves
    // - whether a player has proven their own board had 10 ships
    address payable player1 = address(0);
    address payable player2 = address(0);
    bool gameOver = false;
    uint timerStart;
    uint timerEnd;
    bool checked_ship;

    mapping (address => uint) internal playersBids;
    mapping (address => bytes32) internal boardCommitments;
    mapping (address => uint) internal provedHits;
    mapping (address => uint) internal provedShips;
    mapping (address => bool) internal playerLeft;

    /*struct State{
        address payable player1;
        address payable player2;
        bool gameOver;
        uint timerStart;
        uint timerEnd;
        bool left;
    }
    State internal actualState;
    State[] internal states;*/
    // Declare events here.
    // Consider triggering an event upon accusing another player of having left.
    event OpponentLeft(address who);
    // Store the bids of each player
    // Start the game when both bids are received
    // The first player to call the function determines the bid amount.
    // Refund excess bids to the second player if they bid too much.
    function store_bid() public payable{
        if (player1 == address(0)){
            player1 = msg.sender;
            playersBids[player1] = msg.value;
        }
        else if(player2 == address(0)){
            player2 = msg.sender;
            playersBids[player2] = msg.value;
        }
        if(player1 != address(0) && player2 != address(0)){
            require(playersBids[player2] >= playersBids[player1], "Player1 bids more than Player2");
            uint valueRefund = playersBids[player2] - playersBids[player1];
            if (valueRefund > 0){
                (bool sent, /*bytes memory data*/) = player2.call{value: address(this).balance}("");
                require(sent, "Failed to send Ether");
            }
            gameOver = false;
        }
    }

    // Clear state - make sure to set that the game is not in session
    function clear_state() internal {
        require(gameOver, "game is still in session");
        playersBids[player1] = 0;
        playersBids[player2] = 0;
        provedHits[player1] = 0;
        provedHits[player2] = 0;
        provedShips[player1] = 0;
        provedShips[player2] = 0;
        boardCommitments[player1] = 0;
        boardCommitments[player2] = 0;
        player1 = address(0);
        player2 = address(0);
    }

    // Store the initial board commitments of each player
    // Note that merkle_root is the hash of the topmost value of the merkle tree
    function store_board_commitment(bytes32 merkle_root) public {
        require(msg.sender == player1 || msg.sender == player2, "not valid adress");
        boardCommitments[msg.sender] = merkle_root;
    }

    // Verify the placement of one ship on a board
    // opening_nonce - corresponds to web3.utils.fromAscii(JSON.stringify(opening) + JSON.stringify(nonce)) in JS
    // proof - a list of sha256 hashes you can get from get_proof_for_board_guess
    // guess_leaf_index - the index of the guess as a leaf in the merkle tree
    // owner - the address of the owner of the board on which this ship lives
    function check_one_ship(bytes memory opening_nonce, bytes32[] memory proof,
        uint256 guess_leaf_index, address owner) public returns (bool result) {
        checked_ship =  verify_opening(opening_nonce, proof, guess_leaf_index, boardCommitments[owner]);
        if(owner == msg.sender && checked_ship){
            provedShips[msg.sender] += 1;
        }
        else if(checked_ship){
            provedHits[msg.sender] += 1;
        }
        result = checked_ship;
        return result;
    }

    // Claim you won the game
    // If you have checked 10 winning moves (hits) AND you have checked
    // 10 of your own ship placements with the contract, then this function
    // should transfer winning funds to you and end the game.
    function claim_win() public {
        require(provedShips[msg.sender] == 10 && provedHits[msg.sender] == 10, "not enought hits or placed ships");
        (bool sent, /*bytes memory data*/) = msg.sender.call{value: address(this).balance}("");
        require(sent, "Failed to send Ether");
        gameOver = true;
        clear_state();
    }

    // Forfeit the game
    // Regardless of cheating, board state, or any other conditions, this function
    // results in all funds being sent to the opponent and the game being over.
    function forfeit(address payable opponent) public {
        require((msg.sender == player1 || msg.sender == player2) && (opponent == player1 || opponent == player2), "invalid address");
        (bool sent, /*bytes memory data*/) = opponent.call{value: address(this).balance}("");
        require(sent, "Failed to send Ether");
        gameOver = true;
        clear_state();
    }

    // Claim the opponent cheated - if true, you win.
    // opening_nonce - corresponds to web3.utils.fromAscii(JSON.stringify(opening) + JSON.stringify(nonce)) in JS
    // proof - a list of sha256 hashes you can get from get_proof_for_board_guess (this is what the sender believes to be a lie)
    // guess_leaf_index - the index of the guess as a leaf in the merkle tree
    // owner - the address of the owner of the board on which this ship lives
    function accuse_cheating(bytes memory opening_nonce, bytes32[] memory proof,
        uint256 guess_leaf_index, address owner) public returns (bool result) {
        require((msg.sender == player1 || msg.sender == player2) && (owner == player1 || owner == player2));
        result = verify_opening(opening_nonce, proof, guess_leaf_index, boardCommitments[owner]);
        if (!result){
            (bool sent, /*bytes memory data*/) = msg.sender.call{value: address(this).balance}("");
            require(sent, "Failed to send Ether");
        }
        
        return result;
    }

    // Claim the opponent of taking too long/leaving
    // Trigger an event that both players should listen for.
    function claim_opponent_left(address opponent) public {
        require(!playerLeft[opponent] && !playerLeft[msg.sender] && (opponent == player1 || opponent == player2), "invalid address or you have to handle a timeout accusation");
        timerStart = now;
        timerEnd = timerStart + 60;
        playerLeft[opponent] = true;
        emit OpponentLeft(opponent);
    }

    // Handle a timeout accusation - msg.sender is the accused party.
    // If less than 1 minute has passed, then set state appropriately to prevent distribution of winnings.
    // Otherwise, do nothing.
    function handle_timeout(address payable opponent) public {
        require(now <= timerEnd && (msg.sender == player1 || msg.sender == player2),"time has run out or invalid address");
        playerLeft[msg.sender] = false;
    }

    // Claim winnings if opponent took too long/stopped responding after claim_opponent_left
    // The player MUST claim winnings. The opponent failing to handle the timeout on their end should not
    // result in the game being over. If the timer has not run out, do nothing.
    function claim_timeout_winnings(address opponent) public {
        require(playerLeft[opponent] && now >= timerEnd, "timer has not run out");
        (bool sent, /*bytes memory data*/) = msg.sender.call{value: address(this).balance}("");
        require(sent, "Failed to send Ether");
        gameOver = true;
        clear_state();
    }

    // Check if game is over
    // Hint - use a state variable for this, so you can call it from JS.
    // Note - you cannot use the return values of functions that change state in JS.
    function is_game_over() public view returns (bool) {
        return gameOver;
    }

    function get_players() public view returns (address, address){
        return (player1, player2);
    }

    function get_checked_ship() public view returns (bool){
        return checked_ship;
    }

    function get_ships_count() public view returns (uint){
        return provedShips[msg.sender];
    }

    function get_player_bid() public view returns (uint){
        return playersBids[msg.sender];
    }

    /**** Helper Functions below this point. Do not modify. ****/
    /***********************************************************/

    function merge_bytes32(bytes32 a, bytes32 b) pure public returns (bytes memory) {
        bytes memory result = new bytes(64);
        assembly {
            mstore(add(result, 32), a)
            mstore(add(result, 64), b)
        }
        return result;
    }

    // Verify the proof of a single spot on a single board
    // \args:
    //      opening_nonce - corresponds to web3.utils.fromAscii(JSON.stringify(opening) + JSON.stringify(nonce)));
    //      proof - list of sha256 hashes that correspond to output from get_proof_for_board_guess()
    //      guess - [i, j] - guess that opening corresponds to
    //      commit - merkle root of the board
    function verify_opening(bytes memory opening_nonce, bytes32[] memory proof, uint guess_leaf_index, bytes32 commit) public view returns (bool result) {
        bytes32 curr_commit = keccak256(opening_nonce); // see if this changes hash
        uint index_in_leaves = guess_leaf_index;

        uint curr_proof_index = 0;
        uint i = 0;

        while (curr_proof_index < proof.length) {
            // index of which group the guess is in for the current level of Merkle tree
            // (equivalent to index of parent in next level of Merkle tree)
            uint group_in_level_of_merkle = index_in_leaves / (2**i);
            // index in Merkle group in (0, 1)
            uint index_in_group = group_in_level_of_merkle % 2;
            // max node index for currrent Merkle level
            uint max_node_index = ((BOARD_LEN * BOARD_LEN + (2**i) - 1) / (2**i)) - 1;
            // index of sibling of curr_commit
            uint sibling = group_in_level_of_merkle - index_in_group + (index_in_group + 1) % 2;
            i++;
            if (sibling > max_node_index) continue;
            if (index_in_group % 2 == 0) {
                curr_commit = keccak256(merge_bytes32(curr_commit, proof[curr_proof_index]));
                curr_proof_index++;
            } else {
                curr_commit = keccak256(merge_bytes32(proof[curr_proof_index], curr_commit));
                curr_proof_index++;
            }
        }
        return (curr_commit == commit);

    }
}
