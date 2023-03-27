pragma solidity ^0.8.0;

contract FederatedLearning {
    struct Model {
        address owner;
        bytes weights;
    }
    struct ModelScore {
        address owner;
        uint256 score;
    }

    enum State {
        Polling,
        Validating
    }

    // State Variables
    State public state;
    Model public globalModel;
    uint256 public periodStart;

    mapping(address => bool) private validated;
    mapping(address => Model) private models;
    mapping(address => uint256) private cummulativeScores;

    // Constants
    uint256 constant pollPeriod = 60 * 50;
    uint256 constant validatePeriod = 60 * 10;

    constructor() {
        globalModel = Model(msg.sender, "0x0");
        periodStart = block.timestamp;
    }

    function setState() public {
        uint256 period = block.timestamp - periodStart;
        if (state == State.Polling && period > pollPeriod) {
            state = State.Validating;
        } else if (state == State.Validating && period > validatePeriod) {
            transition();
            state = State.Polling;
        } else return;
        periodStart = block.timestamp;
    }

    modifier onlyPolling() {
        setState();
        require(state == State.Polling);
        _;
    }

    modifier onlyValidating() {
        setState();
        require(state == State.Validating);
        _;
    }

    function sendModel(bytes calldata weights) external onlyPolling {
        models[msg.sender] = Model(msg.sender, weights);
    }

    function sendValidation(ModelScore[] calldata scores)
        external
        onlyValidating
        returns (bool)
    {
        if (validated[msg.sender]) return false;
        validated[msg.sender] = true;

        for (uint256 i = 0; i < scores.length; i++) {
            cummulativeScores[scores[i].owner] += scores[i].score;
        }

        return true;
    }

    // Transition from one cycle (polling followed by validation) to the next 
    // That is update the 
    function transition() private {
        // :TODO
    }
}
