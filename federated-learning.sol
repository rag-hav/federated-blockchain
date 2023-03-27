// SPDX-License-Identifier: BSD-3-Clause-Modification
pragma solidity ^0.8.0;

contract FederatedLearning {
    struct Model {
        uint256 roundNo;
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
    uint256 public roundNo;
    uint256 public periodStart;

    mapping(uint256 => mapping(address => bool)) private hasValidated;
    mapping(uint256 => mapping(address => Model)) private models;
    mapping(uint256 => mapping(address => uint256)) private cummulativeScores;
    mapping(uint256 => uint256) private totalModels;
    mapping(uint256 => uint256) private totalValidations;

    // Constants
    uint256 constant pollPeriod = 60 * 50;
    uint256 constant validatePeriod = 60 * 10;

    constructor() {
        roundNo = 1;
        globalModel = Model(1, msg.data);
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

    function sendModel(bytes calldata weights)
        external
        onlyPolling
        returns (bool)
    {
        if (models[roundNo][msg.sender].roundNo < roundNo) {
            models[roundNo][msg.sender] = Model(roundNo, weights);
            totalModels[roundNo]++;
            return true;
        }
        return false;
    }

    function sendValidation(ModelScore[] calldata scores)
        external
        onlyValidating
        returns (bool)
    {
        if (!hasValidated[roundNo][msg.sender] && scores.length == totalModels[roundNo]) {
            hasValidated[roundNo][msg.sender] = true;
            totalValidations[roundNo]++;

            for (uint256 i = 0; i < scores.length; i++) {
                cummulativeScores[roundNo][scores[i].owner] += scores[i].score;
            }
            return true;
        }

        return false;
    }

    // Transition from one round (polling followed by validation) to the next
    // That is update the scores
    function transition() private {
        roundNo++;
    }
}
