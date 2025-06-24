## 📊 JobSleuth Workflow

```mermaid
flowchart TD
    A[Telegram / Job Boards / RSS] --> B[Scheduler / Fetcher]
    B --> C[Extractors (NER, Regex, Tagger)]
    C --> D[MongoDB]
    D --> E[FastAPI API Layer]
    E --> F1[Dashboard / Web UI]
    E --> F2[CLI]
    E --> F3[Notification Service / Alerts]
    C -.->|Logging & Error| G[Logger]
    B -.->|Logging & Error| G

    style A fill:#c0e6ff,stroke:#007acc
    style B fill:#ffe7ba,stroke:#fa8c16
    style C fill:#ffd6e7,stroke:#eb2f96
    style D fill:#dcffe4,stroke:#52c41a
    style E fill:#e9eaff,stroke:#2f54eb
    style F1 fill:#f6f1ff,stroke:#722ed1
    style F2 fill:#f6f1ff,stroke:#722ed1
    style F3 fill:#f6f1ff,stroke:#722ed1
    style G fill:#fffbe6,stroke:#faad14
