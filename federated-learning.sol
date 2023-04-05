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
        bool stateLock;
    }

    struct AverageScore {
        uint256 scoreSum;
        uint256 scoreCount;
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
    State public state; // What the contract is doing right now (polling or validation)
    uint256 public roundNo; // Which round it is
    uint256 public roundEnd; // When will the current round end (unix timestamp)
    bool stateLock; // Wether the state is locked, only when atleast one transaction for polling
    // or validation is made the state will be changed

    mapping(uint256 => mapping(address => bool)) private hasValidated;
    mapping(uint256 => mapping(address => Model)) private models;
    mapping(uint256 => address[]) private pollers;
    mapping(uint256 => uint256) validatorsCount;

    // Constants
    uint256 constant POLLING_TIME = 30; // Minimum time for polling
    uint256 constant VALIDATION_TIME = 30; // Minimum time for validation
    uint256 constant MAX_SCORE = 1000000; // Maximum score one validator can give to one model
    uint256 constant MAX_DATABASE_SIZE = 1000000; // Maximum database size a validator can claim

    constructor(bytes memory initialWeights) {
        // Intialize the global model
        roundNo = 0;

        // For round 0, store the initialWeights as the only model which was stored during polling
        // This is to make the code to get global model for round 1 same as any other round
        models[roundNo][msg.sender] = Model({
            owner: msg.sender,
            weights: initialWeights,
            score: MAX_SCORE,
            state: ModelState.Created
        });
        pollers[roundNo].push(msg.sender);

        roundNo++;
        stateLock = true;
        roundEnd = block.timestamp + POLLING_TIME;
    }

    function setState() public {
        if (!stateLock && block.timestamp >= roundEnd) {
            if (state == State.Polling) {
                roundEnd = block.timestamp + VALIDATION_TIME;
                state = State.Validating;
            } else {
                roundNo++;
                roundEnd = block.timestamp + POLLING_TIME;
                state = State.Polling;
            }
            stateLock = true;
        }
    }

    function sendModel(bytes calldata weights) external {
        setState();
        require(state == State.Polling);

        // A node can submit a model only once during a polling round
        require(models[roundNo][msg.sender].state == ModelState.NotCreated);

        models[roundNo][msg.sender] = Model({
            owner: msg.sender,
            weights: weights,
            score: 0,
            state: ModelState.Created
        });
        pollers[roundNo].push(msg.sender);

        stateLock = false;
        setState();
    }

    function sendValidation(ModelScore[] calldata scores, uint256 sampleCount)
        external
    {
        setState();
        require(state == State.Validating);
        // A node can only validate models once
        require(!hasValidated[roundNo][msg.sender]);
        require(scores.length == pollers[roundNo].length);

        for (uint256 i = 0; i < scores.length; i++) {
            models[roundNo][scores[i].owner].state = ModelState.Validated; // Temporarily marking models
        }

        bool hasAllModels = true;
        for (uint256 i = 0; i < pollers[roundNo].length; i++) {
            address modelAdd = pollers[roundNo][i];
            if (models[roundNo][modelAdd].state != ModelState.Validated)
                // Model is not included in scores
                hasAllModels = false;
            models[roundNo][modelAdd].state = ModelState.Created;
        }

        // All models stored during polling must be scored
        require(hasAllModels);

        hasValidated[roundNo][msg.sender] = true;
        for (uint256 i = 0; i < scores.length; i++) {
            models[roundNo][scores[i].owner].score +=
                scores[i].score *
                sampleCount; // Potential Security risk, bad actor can claim high sample count
        }

        validatorsCount[roundNo]++;
        stateLock = false;
        setState();
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
        Model[] memory modelList = new Model[](pollers[x].length);

        for (uint256 i = 0; i < pollers[x].length; i++) {
            address modelAdd = pollers[x][i];
            modelList[i] = models[x][modelAdd];
        }

        return modelList;
    }

    function getState() external view returns (ContractState memory) {
        return
            ContractState({
                state: state,
                roundNo: roundNo,
                roundEnd: roundEnd,
                stateLock: stateLock
            });
    }

    function getAverageScore(uint256 x)
        external
        view
        returns (AverageScore memory)
    {
        // Average score only possible for present or past rounds
        require(x <= roundNo);

        uint256 totalScore = 0;

        for (uint256 i = 0; i < pollers[x].length; i++) {
            totalScore += models[x][pollers[x][i]].score;
        }

        return
            AverageScore({
                scoreSum: totalScore,
                scoreCount: pollers[x].length * validatorsCount[x]
            });
    }
}
