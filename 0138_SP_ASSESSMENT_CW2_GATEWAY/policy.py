from blacklist import add_to_blacklist


def execute_policy(agent_decision):
    action = agent_decision.recommended_action.lower()

    final_action = action
    quarantine_applied = False

    if action == "block" and agent_decision.risk_level == "high":
        add_to_blacklist(agent_decision.device_id)
        quarantine_applied = True
        final_action = "block_and_quarantine"

    elif action == "flag":
        final_action = "flag_for_review"

    elif action == "allow":
        final_action = "allow"

    return {
        "final_action": final_action,
        "quarantine_applied": quarantine_applied
    }