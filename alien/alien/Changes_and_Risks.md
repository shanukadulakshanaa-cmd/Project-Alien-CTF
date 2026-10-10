# Member 4 - Integration, Testing & Documentation

## 1. Design Changes (Assignment 1 vs Actual Implementation)

### Change 01: Python Version
- **Original Design:** Planned to use Python 3.11 for the web applications[cite: 14].
- **Implemented Change:** Used the `python:3.9-slim` base image in the Docker containers[cite: 48].
- **Justification:** This change was made to reduce the Docker image size and ensure better module compatibility[cite: 2, 3].

### Change 02: [Oyalage wena wenaskamak liyanna]
* **Original Design:** [Kalin thibba widiya liyanna]
* **Implemented Change:** [Dan hadala thiyena widiya liyanna]
* **Justification:** [Wenas karanna hethuwa liyanna]

---

## 2. Risk Register Outcomes

### Risk R5: Port Conflicts
* **Expected Risk:**  Ports 9000 and 9001 conflicting with other applications.
* **Outcome:** During testing, port 9000 was already in use by another application.
* **Mitigation:** Provided clear instructions in the INSTALLATION.txt file on how to change the port numbers.

### Risk R8: Docker Pull Issues
* **Expected Risk:** Internet disconnection while pulling Docker images.
* **Outcome:** Testing welawedi internet awulak awe naha.
* **Mitigation:** Awulak awath meka offline run wena hinda prashnayak naha kiyala thahawuru kara.

### Risk [Risk Number eka danna]: [Risk eke nama danna]
* **Expected Risk:** [Prashne mokakda kiyala liyanna]
* **Outcome:** [Test karaddi eka awada kiyala liyanna]
* **Mitigation:** [Eka wisandapu widiya liyanna]