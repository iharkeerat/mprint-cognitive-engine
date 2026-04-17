<div align="center">

# 🧠 M-Print — Cognitive Intelligence Engine
**Modeling how learners think — not just what they know.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Database](https://img.shields.io/badge/Graph_DB-Neo4j-018bff?logo=neo4j)](https://neo4j.com/)
[![AI Engine](https://img.shields.io/badge/AI-Gemini_2.5_Flash-8A2BE2)](#)

</div>

## 🚀 Overview

Most educational systems evaluate knowledge outcomes — what a learner remembers. **M-Print** explores a different direction: *Can we model how learners think while learning?*

This project is a cognitive intelligence engine built at the intersection of:  
**Artificial Intelligence × Graph Theory × Educational Psychology**

Instead of focusing solely on correctness, M-Print attempts to model real-time cognitive processes through behavioral signals and adaptive pathways.

---

## 🎯 Core Idea

The system does not label the learner. It continuously learns *how* the learner learns. M-Print captures interaction-level data to approximate:

- ⚡ **Behavioral engagement velocity**
- 🧠 **Information internalization patterns**
- 🔄 **Dynamic learning pathway adaptation**

---

## 🧠 System Architecture

### 🔹 Generative AI as Analytic Engine
Orchestrates Google Gemini 2.5 Flash as a structured reasoning layer, generating real-time adaptive diagnostics with strict JSON enforcement and schema validation.

### 🔹 Graph-Theoretic Pathway Optimization
A Neo4j-based knowledge graph models conceptual dependencies and identifies optimal prerequisite pathways for efficient learning progression.

### 🔹 Behavioral Analytics
Captures millisecond-level interaction signals (response time, accuracy trends) to approximate cognitive patterns such as:
- **Activist**
- **Reflector**
- **Theorist**
- **Pragmatist**

---

## ⚙️ Tech Stack & Implementation

| Component | Technologies | Description |
| :--- | :--- | :--- |
| **Backend** | FastAPI (Python) | Orchestrates AI inference, graph traversal, and behavioral data pipelines. |
| **Databases** | Neo4j, SQLite | Neo4j for the knowledge graph; SQLite for time-series behavioral logs. |
| **Frontend** | Tailwind CSS, Three.js, Chart.js | Glassmorphism UI integrated with WebGL and Chart.js for real-time visualization. |
| **Security** | JWT, bcrypt | Stateless JWT authentication with bcrypt-based password hashing. |

---

## 📊 Intelligence Model

### Metrics
- **Confidence Score:** `Correct / Total`
- **Learning Velocity:** Improvement rate over time
- **Behavioral Consistency:** Interaction stability across sessions

### Behavioral Interpretation
| Signal | Interpretation |
| :--- | :--- |
| ⚡ **Fast + Incorrect** | Indicates impulsive response patterns. |
| 🐢 **Slow + Correct** | Indicates reflective and deliberate thinking. |
| 🔄 **Repeated Errors** | Suggests underlying conceptual weakness. |

---

## 🗄️ Data Design

Core entities tracked within the system:
- `Users` → Profile, goals, context.
- `Sessions` → Topic interactions, timestamps.
- `Performance` → Correctness, time taken.
- `Insights` → Patterns, weak areas, scores.

---

## 🔬 Research Perspective

M-Print is an exploratory system that attempts to translate pedagogical concepts into computational models. It reflects a broader shift:

> **From static learning systems → to adaptive, cognitively-aware intelligence systems.**

This work is not a complete solution, but an evolving attempt to bridge AI systems, human cognition, and learning sciences.

---

## 🚀 Future Scope

- [ ] Machine learning–based cognitive prediction
- [ ] Dropout risk detection
- [ ] Personalized long-term learning pathways
- [ ] Deeper validation of behavioral models
- [ ] Research publication

---

## ⚠️ Limitations

- Cognitive modeling is approximate, not definitive.
- Behavioral signals may not fully capture learning depth.
- Requires further empirical validation.

---

## 🤝 Contributing

Contributions, ideas, and critiques are welcome. Feel free to open issues or submit pull requests to help evolve this engine.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **Apache License 2.0**.  
You are free to use, modify, and distribute this software with proper attribution. See the `LICENSE` file for details.

---

## 🙏 Acknowledgements

Grateful to the open-source communities behind:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Neo4j](https://neo4j.com/)
- [Three.js](https://threejs.org/)
