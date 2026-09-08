# GitHub Repositories & Project Source Code Digest

**Author:** Vince Nguyen (`@VinceNguyen000`)  
**GitHub Profile:** [https://github.com/VinceNguyen000](https://github.com/VinceNguyen000)

---

## 1. Repository: `2026-agentic-ai-job-search`

- **URL:** [https://github.com/VinceNguyen000/2026-agentic-ai-job-search](https://github.com/VinceNguyen000/2026-agentic-ai-job-search)
- **Primary Languages:** Python (100%)
- **Domain:** Autonomous AI Agents, Multi-Criteria Optimization, Information Retrieval
- **Description:** An autonomous, multi-agent AI job matching and career advancement platform built using Antigravity and Python.
- **Key Modules & Architecture:**
  - `src/agent.py`: `JobSearchAgent` engine equipped with 6 discrete tool capabilities (`get_seeker_profile`, `search_opportunities`, `evaluate_fit`, `analyze_skill_gaps`, `draft_tailored_application`, `generate_upskilling_roadmap`).
  - `src/matcher.py`: 7-factor weighted scoring algorithm evaluating Skills (30%), Experience (25%), Location (15%), Salary (15%), Work Mode (5%), Work Type (5%), and Career Goals (5%).
  - `src/utils.py`: Keyword containment tokenization with stopword filtering, 2-letter tech acronym alias expansion (`AI`, `ML`, `JS`, `DB`), and interval salary math.
  - `tests/`: Zero-dependency 17-test unit suite with 100% test pass rate.

---

## 2. Project: `Secure-Web-Application-with-Vulnerability-Assessment`

- **Primary Languages / Tools:** Python, Flask, Kali Linux, Nmap, SQLMap, GVM (Greenbone), Metasploit
- **Domain:** Application Security (AppSec), Penetration Testing, Threat Mitigation
- **Description:** A hardened web application coupled with full-cycle vulnerability scanning and penetration testing.
- **Key Technical Highlights:**
  - Designed secure backend routing with Flask that prevents common injection attacks (SQLi, Reflected/Stored XSS).
  - Configured automated security scanning workflows with Nmap for port/service auditing, SQLMap for database security verification, and GVM for comprehensive CVE detection.
  - Formulated remediation patches strictly aligned with OWASP Top 10 guidelines and documented security post-mortems.

---

## 3. Project: `Personal-Blog-Platform`

- **Primary Languages / Tools:** PHP, Laravel, MySQL, Tailwind CSS, XAMPP, Git, Mailchimp API
- **Domain:** Full-Stack Web Engineering, Database Design, IAM
- **Description:** A production-style dynamic content management system and blogging platform.
- **Key Technical Highlights:**
  - Designed and implemented normalized relational MySQL database schemas with indexing on tags and categories.
  - Built secure authentication, session handling, password hashing, and role-based access control (RBAC).
  - Integrated third-party webhook and Mailchimp REST APIs for automated newsletter distribution.

---

## 4. Research Work: `BLE-IoT-Vulnerability-Analysis`

- **Primary Tools:** Wireshark, BLE Sniffers, Linux Network Utilities, Python
- **Domain:** IoT Security, Wireless Protocol Analysis, Exploitation Defense
- **Description:** Academic research at UMKC investigating security posture of commercial IoT asset tags.
- **Key Technical Highlights:**
  - Captured and analyzed BLE advertising and connection packets to detect cleartext authentication exchanges.
  - Modeled replay attack vectors and quantified exposure levels across varying wireless distances.
  - Documented protocol hardening recommendations to mitigate wireless device hijacking.
