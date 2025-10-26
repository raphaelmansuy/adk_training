def test_root_agent_instruction_constraints():
    path = "tutorial_implementation/commerce_agent_e2e/commerce_agent/agent.py"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # The instruction must explicitly forbid the literal phrase in outputs
    assert (
        'Do NOT print the literal phrase: Engaging Narrative:' in text
        or 'do NOT include the exact literal header or phrase "Engaging Narrative:"' in text
    ), "Agent instruction does not explicitly forbid the literal phrase in outputs"

    # The instruction must require saving preferences and acknowledging
    assert "ALWAYS call the Preference Manager" in text or "Preferences saved." in text, (
        "Preference Manager save instruction or confirmation not found in agent instruction"
    )

    # The instruction must require using exact URLs from search results
    assert "use REAL URLs copied from search results" in text or "use only URLs present in search results" in text, (
        "URL provenance requirement not found in agent instruction"
    )

    print("Instruction constraints present and OK")
