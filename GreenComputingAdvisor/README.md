# Green Computing Advisor

A rule-based expert system for an Artificial Cognitive Systems coursework project.

## Expert-system features
- 30 production rules in a separate knowledge base
- Working memory containing user-supplied facts
- Generic forward-chaining inference engine
- Rule trace / WHY explanation facility
- Priority-based recommendation ordering
- Energy and optional CO2e calculation
- Transparent heuristic Green Score
- Test cases

## Architecture
User Interface -> Working Memory -> Inference Engine <-> Knowledge Base -> Recommendations / Explanation

## Run
Requires Python 3.10+.

From the project folder in PowerShell:

```powershell
Set-Location "C:\Users\pc\Documents\GreenComputingAdvisor\GreenComputingAdvisor"
python -m venv ..\.venv
. "..\.venv\Scripts\Activate.ps1"
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Test
```powershell
Set-Location "C:\Users\pc\Documents\GreenComputingAdvisor\GreenComputingAdvisor"
. "..\.venv\Scripts\Activate.ps1"
pytest -q
```

## Reasoning model
Each rule contains conditions and a conclusion. The inference engine repeatedly matches conditions against working memory. When a rule fires, its conclusion is inserted into working memory and its trace is recorded. The cycle continues until no new rule can fire (forward chaining).

## Equations
Energy (kWh) = Power (W) × Time (h) / 1000

CO2e (kg) = Energy (kWh) × Carbon intensity (kg CO2e/kWh)

Carbon intensity is deliberately entered by the user rather than hard-coded because it depends on electricity source, region and time.

## Green Score
The application starts at 100 and subtracts explicit heuristic penalties for matched inefficiency rules:
- High priority: normally 10
- Medium: normally 5
- Low: normally 3

This score is a coursework heuristic, not a recognized environmental certification.

## Suggested demonstration
1. Show `knowledge_base/rules.py` and explain production rules.
2. Enter an inefficient laptop scenario.
3. Run the assessment.
4. Show which rules fired.
5. Click "Why did the rule fire?".
6. Explain working memory and forward chaining.
7. Demonstrate an AI/ML scenario.
8. Explain the energy equation and configurable carbon intensity.

## Important
Recommendations are educational and rule-based. Actual energy savings depend on hardware, workload, configuration and electricity supply. Validate recommendations before applying them to production systems.
