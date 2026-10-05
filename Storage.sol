// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 * @custom:dev-run-script ./scripts/deploy_with_ethers.ts
 */
contract Storage {
    uint256 private number;
    uint256 public studentId;
    address public owner;

    // Access control modifier restricting functions to the contract owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Access denied: Caller is not the owner");
        _;
    }

    // Set the contract deployer as the initial owner
    constructor() {
        owner = msg.sender;
    }

    // --- Original Storage Functions ---

    /**
     * @dev Store value in variable
     * @param num value to store
     */
    function store(uint256 num) public {
        number = num;
    }

    /**
     * @dev Return value
     * @return value of 'number'
     */
    function retrieve() public view returns (uint256) {
        return number;
    }

    // --- New Variable & Access Control Functions ---

    /**
     * @dev Updates the student ID. Only the contract owner can call this function.
     * @param _studentId The new student ID number to store.
     */
    function setStudentId(uint256 _studentId) public onlyOwner {
        studentId = _studentId;
    }
}
