// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract FileStorage {
    address public admin;

    struct File {
        string regNo;
        string userEmail;
        string fileHash;
        bool exists;
    }

    mapping(string => File[]) public filesByUser;

    event FileStored(string regNo, string userEmail, string fileHash);
    event NewUserCreated(string userEmail);

    // modifier onlyAdmin() {
    //     require(msg.sender == admin, "Only the admin can call this function");
    //     _;
    // }

    // constructor() {
    //     admin = msg.sender;
    // }

    function storeFile(string memory regNo, string memory userEmail, string memory fileHash) external  {
        File[] storage userFiles = filesByUser[userEmail];

        bool found = false;
        for (uint256 i = 0; i < userFiles.length; i++) {
            if (keccak256(abi.encodePacked(userFiles[i].regNo)) == keccak256(abi.encodePacked(regNo))) {
                userFiles[i].fileHash = fileHash;
                userFiles[i].exists = true;
                found = true;
                break;
            }
        }

        if (!found) {
            File memory newFile = File(regNo, userEmail, fileHash, true);
            filesByUser[userEmail].push(newFile);
            emit NewUserCreated(userEmail);
        }

        emit FileStored(regNo, userEmail, fileHash);
    }

    function getFile(string memory regNo, string memory userEmail) external view returns (string memory, string memory, string memory) {
        File[] memory userFiles = filesByUser[userEmail];

        for (uint256 i = 0; i < userFiles.length; i++) {
            if (keccak256(abi.encodePacked(userFiles[i].regNo)) == keccak256(abi.encodePacked(regNo))) {
                return (userFiles[i].regNo, userFiles[i].userEmail, userFiles[i].fileHash);
            }
        }

        revert("File not found for the given user and registration number");
    }

    function userExists(string memory userEmail) external view returns (bool) {
        File[] memory userFiles = filesByUser[userEmail];
        return userFiles.length > 0;
    }

    function getFilesByUser(string memory userEmail) external view returns (File[] memory) {
        return filesByUser[userEmail];
    }
}
