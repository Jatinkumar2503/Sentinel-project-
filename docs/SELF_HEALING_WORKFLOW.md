# Autonomous Self-Healing Workflow

## Operational Pipeline
1. **Health Degradation**: When a collection run's Health Score falls below 70%, Sentinel AI initiates the healing state machine.
2. **DOM AST & Root Cause Analysis**: The engine parses target HTML and identifies failing selector nodes.
3. **Selector Synthesis**: Heuristic and Bright Data AI strategies synthesize replacement selectors (e.g. converting broken `.price` to `[data-testid="price"]`).
4. **Sandbox Execution**: The collector re-runs in an isolated environment using the candidate selector manifest.
5. **Validation Gateway**: Verifies candidate output against structural, statistical, and business invariants.
6. **Promotion & Broadcasting**: Restored selectors are promoted to production and streamed live over WebSockets.
