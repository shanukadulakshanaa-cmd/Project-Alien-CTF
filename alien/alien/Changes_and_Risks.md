# Member 4 - Integration, Testing & Documentation

## 1. Design Changes (Assignment 1 vs Actual Implementation)

### Change 01: Python Version
- **Original Design:** Planned to use Python 3.11 for the web applications[cite: 14].
- **Implemented Change:** Used the `python:3.9-slim` base image in the Docker containers[cite: 48].
- **Justification:** This change was made to reduce the Docker image size and ensure better module compatibility[cite: 2, 3].

### Change 02: Flag Format Update
* **Original Design:** In Assignment 1, it was planned to use the standard "ctf" flag format.
* **Implemented Change:** During the implementation phase, this was changed to use the "alian" flag format.
* **Justification:** To better align with the specific theme and requirements of the challenges.

---

## 2. Risk Register Outcomes

### Risk R5: Port Conflicts
* **Expected Risk:**  Ports 9000 and 9001 conflicting with other applications.
* **Outcome:** During testing, port 9000 was already in use by another application.
* **Mitigation:** Provided clear instructions in the INSTALLATION.txt file on how to change the port numbers.
### Risk R7: Version Incompatibility in Exploit Tools
* **Expected Risk:** Players run into version incompatibility issues with pwntools or GDB on Stage 06.
* **Outcome:** The solve.py exploit script was tested and executed end-to-end successfully without any dependency failures during validation.
* **Mitigation:** Documented the exact tool versions needed, and players can analyze the file safely using the recommended environments like Kali Linux.
### Risk R8: Docker Pull Issues
* **Expected Risk:** Internet disconnection while pulling Docker images.
* **Outcome:** No internet connectivity issues occurred during the testing phase.
* **Mitigation:** Confirmed that even in the event of an internet disruption, it would not cause a problem because the system runs entirely offline.
### Risk R9: System File Corruption within Containers
* **Expected Risk:** Players mess up the system files inside a container and break the challenge.
* **Outcome:** System recovery testing (recovery_test.sh) confirmed that crashing or modifying container files does not affect the host, and the system can be restored instantly.
* **Mitigation:** The containers are designed to be stateless. Running the recovery script cleanly resets the Docker environment.