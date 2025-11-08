"""
Vulnerability Lifecycle Workflow Integration
Story 3.4: Integrates priority-based review triggering into complete vulnerability lifecycle

This module orchestrates the transition from enrichment to review or remediation
based on priority and sampling rules defined in Story 3.4.
"""

import logging
from workflows.review_trigger import (
    determine_review_requirement,
    assign_reviewer,
    notify_reviewer,
    log_review_decision,
    update_review_decision_reviewer
)


# Configure logging
logging.basicConfig(level=logging.INFO)


def post_enrichment_workflow(ticket, jira_client):
    """
    Determine next step after enrichment based on priority and sampling rules

    This function is called after security alert enrichment completes (Story 3.1).
    It implements the priority-based review triggering logic from Story 3.4.

    Args:
        ticket: Ticket object with priority attribute and other metadata
        jira_client: JIRA client instance for API operations

    Workflow:
        1. Determine if review is required based on priority and sampling
        2. If review required:
           - Transition ticket to "In Review" status
           - Assign reviewer based on priority and assignment rules
           - Add JIRA comment explaining review requirement
           - Send notifications to assigned reviewer
           - Log decision for sampling statistics
        3. If review not required:
           - Transition ticket to "Remediation Planning" status
           - Add JIRA comment explaining skip reason
           - Log decision for sampling statistics
    """
    priority = ticket.priority

    # Determine if review required
    review_decision = determine_review_requirement(ticket)

    # Log the decision
    log_review_decision(
        ticket_id=ticket.id,
        priority=priority,
        decision='required' if review_decision.review_required else 'not_required',
        reason=review_decision.reason,
        reviewer=None  # Will be populated after assignment
    )

    if review_decision.review_required:
        # Transition to review
        logging.info(f"Transitioning {ticket.id} to 'In Review' status")
        jira_client.transition_issue(ticket.id, "In Review")

        # Assign reviewer
        reviewer = assign_reviewer(priority, review_decision.assignment_pool)

        # Notify reviewer (includes JIRA assignment)
        notify_reviewer(reviewer, ticket.id, jira_client)

        # Update log with assigned reviewer
        update_review_decision_reviewer(ticket.id, reviewer)

        # Add comment
        comment = f"""🔍 **Review Required**

This {priority} ticket has been assigned for quality assurance review.

**Reason:** {review_decision.reason}
**Assigned Reviewer:** {reviewer}
**Blocking Remediation:** {"Yes" if review_decision.blocking else "No"}
"""
        jira_client.add_comment(ticket.id, comment)
        logging.info(f"Review assigned for {ticket.id} to {reviewer}")

    else:
        # Skip review, proceed to remediation
        logging.info(f"Transitioning {ticket.id} to 'Remediation Planning' status")
        jira_client.transition_issue(ticket.id, "Remediation Planning")

        # Add comment
        comment = f"""✅ **Review Skipped**

This {priority} ticket is proceeding directly to remediation planning.

**Reason:** {review_decision.reason}
"""
        jira_client.add_comment(ticket.id, comment)
        logging.info(f"Review skipped for {ticket.id}, proceeding to remediation")


def handle_review_completion(ticket, review_result, jira_client):
    """
    Handle workflow after QA review completes

    Args:
        ticket: Ticket object
        review_result: Review result object with status and findings
        jira_client: JIRA client instance

    Workflow transitions based on review outcome:
        - Critical Issues → Back to "In Progress" (re-enrichment needed)
        - Approved → "Remediation Planning"
    """
    if review_result.status == 'critical_issues':
        # Review identified critical issues requiring re-enrichment
        logging.warning(f"Critical issues found in {ticket.id}, returning to enrichment")
        jira_client.transition_issue(ticket.id, "In Progress")

        comment = f"""⚠️ **Review Identified Critical Issues**

QA review has identified critical issues requiring re-enrichment.

**Issues Found:**
{review_result.issues_summary}

**Next Steps:** Re-enrichment required before proceeding to remediation.
"""
        jira_client.add_comment(ticket.id, comment)

    elif review_result.status == 'approved':
        # Review approved, proceed to remediation
        logging.info(f"Review approved for {ticket.id}, proceeding to remediation")
        jira_client.transition_issue(ticket.id, "Remediation Planning")

        comment = f"""✅ **Review Approved**

QA review has been completed and approved.

**Reviewer Notes:**
{review_result.notes}

**Next Steps:** Proceed to remediation planning.
"""
        jira_client.add_comment(ticket.id, comment)
