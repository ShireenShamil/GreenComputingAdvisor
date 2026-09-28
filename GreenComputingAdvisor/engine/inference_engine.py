from knowledge_base.rules import RULES

def condition_matches(actual, expected):
    if isinstance(expected, (list, tuple, set)):
        return actual in expected
    return actual == expected

def infer(initial_facts):
    """
    Forward-chaining production-rule engine.
    User observations enter working memory as facts. Matching rules fire,
    recommendations are added as derived facts, and the cycle repeats until
    no new conclusion can be produced.
    """
    working_memory = dict(initial_facts)
    fired = set()
    results = []

    changed = True
    while changed:
        changed = False
        for rule in RULES:
            if rule["id"] in fired:
                continue
            if all(condition_matches(working_memory.get(k), v)
                   for k, v in rule["conditions"].items()):
                fired.add(rule["id"])
                conclusion_key = "recommend_" + rule["id"].lower()
                working_memory[conclusion_key] = rule["conclusion"]
                results.append({
                    **rule,
                    "matched_facts": {
                        k: working_memory.get(k) for k in rule["conditions"]
                    }
                })
                changed = True

    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(results, key=lambda r: (priority_order[r["priority"]], r["id"]))


def backward_chain(goal, facts, visited=None):
    """
    Goal-driven backward-chaining inference.

    Starts with a goal and searches for rules that can
    establish it. Recursively checks rule conditions
    against known facts or other derived conclusions.
    """
    if visited is None:
        visited = set()

    # Avoid infinite recursion if rules depend on each other.
    if goal in visited:
        return {
            "goal": goal,
            "proved": False,
            "reason": "Circular dependency detected.",
            "rules": [],
            "missing_facts": []
        }

    visited = visited | {goal}

    # Check whether the goal is already a known fact.
    if goal in facts:
        return {
            "goal": goal,
            "proved": bool(facts[goal]),
            "reason": "Goal is already present in working memory.",
            "rules": [],
            "missing_facts": []
        }

    # Find rules that can establish this goal.
    candidate_rules = [
        rule for rule in RULES
        if rule["conclusion"] == goal
    ]

    if not candidate_rules:
        return {
            "goal": goal,
            "proved": False,
            "reason": "No rule can establish this goal.",
            "rules": [],
            "missing_facts": [goal]
        }

    all_attempts = []
    all_missing = []

    for rule in candidate_rules:
        rule_proved = True
        rule_steps = []
        rule_missing = []

        for key, expected in rule["conditions"].items():

            actual = facts.get(key)

            # If a condition is known, check it directly.
            if key in facts:
                if not condition_matches(actual, expected):
                    rule_proved = False
                    rule_missing.append(
                        f"{key} must match {expected}; "
                        f"received {actual}"
                    )
                continue

            # Otherwise, try to prove the condition
            # as another derived conclusion.
            if isinstance(expected, (list, tuple, set)):
                subgoals = list(expected)
            else:
                subgoals = [expected]

            subgoal_proved = False

            for subgoal in subgoals:
                sub_result = backward_chain(
                    subgoal, facts, visited
                )

                if sub_result["proved"]:
                    subgoal_proved = True
                    rule_steps.append(sub_result)
                    break

            if not subgoal_proved:
                rule_proved = False
                rule_missing.append(
                    f"Missing or unproven condition: {key}"
                )

        all_attempts.append({
            "rule_id": rule["id"],
            "conclusion": rule["conclusion"],
            "proved": rule_proved,
            "conditions": rule["conditions"],
            "explanation": rule["explanation"],
            "recommendation": rule["recommendation"],
            "substeps": rule_steps,
            "missing_facts": rule_missing
        })

        all_missing.extend(rule_missing)

        if rule_proved:
            return {
                "goal": goal,
                "proved": True,
                "reason": "Goal established by backward chaining.",
                "rules": [all_attempts[-1]],
                "missing_facts": []
            }

    return {
        "goal": goal,
        "proved": False,
        "reason": "The available facts do not establish the goal.",
        "rules": all_attempts,
        "missing_facts": list(dict.fromkeys(all_missing))
    }
