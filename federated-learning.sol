// SPDX-License-Identifier: BSD-3-Clause-Modification
pragma solidity ^0.8.0;

// Each period or round of Federated learning has two phase
// - Polling phase- Nodes send their model
// - Validating Phase - Node validate all models sent during polling phase

contract FederatedLearning {
    struct Model {
        address owner;
        bytes weights;
        uint256 score;
        ModelState state;
    }
    struct ModelScore {
        address owner;
        uint256 score;
    }

    struct GlobalModel {
        uint256 roundNo;
        Model[] models;
    }

    struct ContractState {
        State state;
        uint256 roundNo;
        uint256 roundEnd;
    }

    enum ModelState {
        NotCreated,
        Created,
        Validated
    }

    enum State {
        Polling,
        Validating
    }

    // State Variables
    State public state;
    uint256 public roundNo;
    uint256 public roundEnd;

    mapping(uint256 => mapping(address => bool)) private hasValidated;
    mapping(uint256 => mapping(address => Model)) private models;
    mapping(uint256 => address[]) private modelOwners;

    // Constants
    uint256 constant POLLING_TIME = 30;
    uint256 constant VALIDATION_TIME = 30;
    uint256 constant SCORE_SCALE_FACTOR = 1000000000;

    constructor(bytes memory initialWeights) {
        // Intialize the global model
        roundNo = 0;
        models[roundNo][msg.sender] = Model({
            owner: msg.sender,
            weights: initialWeights,
            score: SCORE_SCALE_FACTOR,
            state: ModelState.Created
        });
        modelOwners[roundNo].push(msg.sender);

        roundNo++;
        roundEnd = block.timestamp + POLLING_TIME;
    }

    function setState() public {
        if (block.timestamp >= roundEnd) {
            if (state == State.Polling) {
                roundEnd = block.timestamp + VALIDATION_TIME;
                state = State.Validating;
            } else {
                roundNo++;
                roundEnd = block.timestamp + POLLING_TIME;
                state = State.Polling;
            }
        }
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
        if (models[roundNo][msg.sender].state == ModelState.NotCreated) {
            models[roundNo][msg.sender] = Model({
                owner: msg.sender,
                weights: weights,
                score: 0,
                state: ModelState.Created
            });
            modelOwners[roundNo].push(msg.sender);
            return true;
        }
        return false;
    }

    function sendValidation(ModelScore[] calldata scores)
        external
        onlyValidating
        returns (bool)
    {

        if (
            hasValidated[roundNo][msg.sender] ||
            scores.length != modelOwners[roundNo].length
        ) return false;

        for (uint256 i = 0; i < scores.length; i++) {
            models[roundNo][scores[i].owner].state = ModelState.Validated;
        }

        bool hasAllModels = true;
        for (uint256 i = 0; i < modelOwners[roundNo].length; i++) {
            address modelAdd = modelOwners[roundNo][i];
            if (models[roundNo][modelAdd].state != ModelState.Validated)
                hasAllModels = false;
            models[roundNo][modelAdd].state = ModelState.Created;
        }

        if (!hasAllModels) return false;

        hasValidated[roundNo][msg.sender] = true;
        for (uint256 i = 0; i < scores.length; i++) {
            models[roundNo][scores[i].owner].score += scores[i].score;
        }
        return true;
    }


    function getGlobalModel() external view returns (GlobalModel memory) {
        uint256 lastRound = roundNo - 1;
        return GlobalModel({roundNo: lastRound, models: getModels(lastRound)});
    }

    function getValidationModels() external view returns (Model[] memory) {
        return getModels(roundNo);
    }

    function getModels(uint256 x) private view returns (Model[] memory) {
        assert(x <= roundNo);
        Model[] memory modelList = new Model[](modelOwners[x].length);

        for (uint256 i = 0; i < modelOwners[x].length; i++) {
            address modelAdd = modelOwners[x][i];
            modelList[i] = models[x][modelAdd];
        }

        return modelList;
    }

    function getState() external view returns (ContractState memory) {
        return ContractState({
            state : state,
            roundNo : roundNo,
            roundEnd : roundEnd
        });
    }
}
