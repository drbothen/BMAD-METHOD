"""
Priority-Based Review Triggering
Story 3.4: Implements mandatory review for P1/P2 and sampling for P3/P4/P5

This module provides core review decision and assignment logic for the
vulnerability lifecycle workflow integration.
"""

import yaml
import os
import random
import logging
import csv
import smtplib
import requests
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Configure logging
logging.basicConfig(level=logging.INFO)


@dataclass
class ReviewDecision:
    """Represents the result of review requirement determination"""
    review_required: bool
    reason: str
    assignment_pool: Optional[str]
    blocking: bool


def load_config(section: str) -> dict:
    """
    Load configuration section from config.yaml

    Args:
        section: Configuration section name (e.g., 'review_triggers', 'reviewer_assignment')

    Returns:
        dict: Configuration for the specified section

    Raises:
        FileNotFoundError: If config.yaml doesn't exist
        KeyError: If section not found in config
        ValueError: If section parameter is invalid
    """
    if not section or not isinstance(section, str):
        raise ValueError(f"Invalid section parameter: {section}")
    # Get the directory where this module is located
    module_dir = os.path.dirname(os.path.abspath(__file__))
    # Config is one level up from workflows/
    config_path = os.path.join(module_dir, '..', 'config.yaml')
    config_path = os.path.normpath(config_path)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    if section not in config:
        raise KeyError(f"Configuration section '{section}' not found in {config_path}")

    return config[section]


def determine_review_requirement(ticket):
    """
    Determine if ticket requires review based on priority and sampling rules

    Args:
        ticket: Ticket object with priority attribute (P1-P5)

    Returns:
        ReviewDecision: Object indicating if review required and assignment details
    """
    priority = ticket.priority  # P1, P2, P3, P4, or P5
    config = load_config("review_triggers")

    trigger_rule = config[priority]

    if trigger_rule['review_required']:
        # Mandatory review (P1/P2)
        return ReviewDecision(
            review_required=True,
            reason=f"Mandatory review for {priority} priority",
            assignment_pool=trigger_rule['assignment'],
            blocking=trigger_rule['blocking']
        )
    else:
        # Sampling-based review (P3/P4/P5)
        random_value = random.random()  # 0.0 to 1.0
        sampling_threshold = trigger_rule['sampling_rate'] / 100.0

        if random_value < sampling_threshold:
            # Selected for review
            return ReviewDecision(
                review_required=True,
                reason=f"Randomly selected for review ({trigger_rule['sampling_rate']}% sampling)",
                assignment_pool=trigger_rule['assignment'],
                blocking=False
            )
        else:
            # Not selected, proceed directly to remediation
            return ReviewDecision(
                review_required=False,
                reason=f"Not selected for review ({trigger_rule['sampling_rate']}% sampling)",
                assignment_pool=None,
                blocking=False
            )


def assign_reviewer(priority: str, assignment_pool: str) -> str:
    """
    Select reviewer based on priority and assignment rules

    Args:
        priority: Priority level (P1-P5)
        assignment_pool: Assignment pool type ('senior-reviewer', 'any-reviewer')

    Returns:
        str: Name of assigned reviewer

    Raises:
        ValueError: If priority is invalid
        KeyError: If priority not found in assignment rules

    Note:
        This is a simplified implementation using hash-based distribution.
        In production, integrate with JIRA user management and workload tracking
        for true round-robin or least-loaded assignment.
    """
    valid_priorities = ['P1', 'P2', 'P3', 'P4', 'P5']
    if priority not in valid_priorities:
        raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")
    config = load_config('reviewer_assignment')
    assignment_rule = config['assignment_rules'][priority]

    # Get eligible reviewers from pool
    pool = assignment_rule['pool']
    method = assignment_rule['method']

    if method == 'least-loaded':
        # TODO: Query JIRA for current workload
        # For now, use simple round-robin as fallback
        reviewer = pool[hash(datetime.utcnow().isoformat()) % len(pool)]
    elif method == 'round-robin':
        # Simple round-robin based on timestamp
        reviewer = pool[hash(datetime.utcnow().isoformat()) % len(pool)]
    else:
        # Default: select first available
        reviewer = pool[0]

    logging.info(f"Assigned reviewer {reviewer} for {priority} ticket using {method} method")
    return reviewer


def notify_reviewer(reviewer, ticket_id, jira_client):
    """
    Send notifications to assigned reviewer via configured channels

    Primary notification (JIRA assignment) always executes.
    Additional channels (email, Slack) are optional and failures are logged but don't block workflow.

    Args:
        reviewer: Reviewer name/username
        ticket_id: JIRA ticket ID (e.g., 'AOD-1234')
        jira_client: JIRA client instance for API operations
    """
    config = load_config('reviewer_assignment')['notification']

    # Primary: JIRA assignment (always executed, uses Atlassian MCP)
    try:
        jira_client.assign_issue(ticket_id, reviewer)
        logging.info(f"JIRA assignment successful for {ticket_id} to {reviewer}")
    except Exception as e:
        logging.error(f"JIRA assignment failed for {ticket_id}: {e}")
        raise  # JIRA assignment failure blocks workflow

    # Optional: Email notification
    if config.get('email', {}).get('enabled', False):
        try:
            send_email_notification(reviewer, ticket_id, config['email'], jira_client)
        except Exception as e:
            log_notification_failure('email', ticket_id, reviewer, e)

    # Optional: Slack notification
    if config.get('slack', {}).get('enabled', False):
        try:
            send_slack_notification(reviewer, ticket_id, config['slack'], jira_client)
        except Exception as e:
            log_notification_failure('slack', ticket_id, reviewer, e)


def send_email_notification(reviewer, ticket_id, email_config, jira_client):
    """Send email notification to reviewer"""
    # Get ticket details for email body
    ticket = jira_client.get_issue(ticket_id)

    # Format email content using template
    subject = email_config['subject_template'].format(
        ticket_id=ticket_id,
        priority=ticket.priority
    )

    body = email_config['body_template'].format(
        ticket_id=ticket_id,
        priority=ticket.priority,
        cve_id=getattr(ticket, 'cve_id', 'N/A'),
        review_type='Mandatory' if ticket.priority in ['P1', 'P2'] else 'Sampling',
        jira_url=f"https://your-org.atlassian.net/browse/{ticket_id}"
    )

    # Create message
    msg = MIMEMultipart()
    msg['From'] = email_config['from_address']
    msg['To'] = f"{reviewer}@example.com"  # Assumes reviewer username maps to email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send via SMTP
    with smtplib.SMTP(email_config['smtp_server'], 587) as server:
        server.starttls()
        # Note: Add authentication if required by your SMTP server
        # server.login(username, password)
        server.send_message(msg)

    logging.info(f"Email notification sent to {reviewer} for {ticket_id}")


def send_slack_notification(reviewer, ticket_id, slack_config, jira_client):
    """Send Slack notification to channel"""
    # Get ticket details for message
    ticket = jira_client.get_issue(ticket_id)

    # Format Slack message using template
    message = slack_config['message_template'].format(
        jira_url=f"https://your-org.atlassian.net/browse/{ticket_id}",
        ticket_id=ticket_id,
        priority=ticket.priority,
        reviewer_name=reviewer,
        review_type='Mandatory' if ticket.priority in ['P1', 'P2'] else 'Sampling'
    )

    # Send webhook POST request
    payload = {
        'text': message,
        'channel': slack_config['channel']
    }

    response = requests.post(
        slack_config['webhook_url'],
        json=payload,
        timeout=10
    )

    response.raise_for_status()
    logging.info(f"Slack notification sent for {ticket_id} to {slack_config['channel']}")


def log_notification_failure(channel, ticket_id, reviewer, error):
    """Log notification failures for troubleshooting"""
    logging.warning(
        f"Notification failure - Channel: {channel}, Ticket: {ticket_id}, "
        f"Reviewer: {reviewer}, Error: {error}"
    )

    # Optionally write to failure log file for analysis
    module_dir = os.path.dirname(os.path.abspath(__file__))
    failure_log = os.path.join(module_dir, '..', 'metrics', 'notification-failures.log')
    failure_log = os.path.normpath(failure_log)
    os.makedirs(os.path.dirname(failure_log), exist_ok=True)
    with open(failure_log, 'a') as f:
        f.write(f"{datetime.utcnow().isoformat()}|{channel}|{ticket_id}|{reviewer}|{error}\n")


def log_review_decision(ticket_id: str, priority: str, decision: str,
                        reason: str, reviewer: Optional[str] = None) -> None:
    """
    Log review decision to CSV for sampling statistics tracking

    Args:
        ticket_id: JIRA ticket ID (e.g., 'AOD-1234')
        priority: Priority level (P1-P5)
        decision: 'required' or 'not_required'
        reason: Human-readable explanation of decision
        reviewer: Assigned reviewer name (None if review not required)

    Raises:
        ValueError: If decision is not 'required' or 'not_required'
    """
    if decision not in ['required', 'not_required']:
        raise ValueError(f"Invalid decision: {decision}. Must be 'required' or 'not_required'")
    module_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(module_dir, '..', 'metrics', 'review-decisions.csv')
    log_path = os.path.normpath(log_path)

    # Ensure metrics directory exists
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Create file with headers if doesn't exist
    if not os.path.exists(log_path):
        with open(log_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ticket_id', 'priority', 'review_decision', 'reason', 'timestamp', 'reviewer'])

    # Append decision
    with open(log_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            ticket_id,
            priority,
            decision,
            reason,
            datetime.utcnow().isoformat() + 'Z',
            reviewer or ''
        ])

    logging.info(f"Logged review decision for {ticket_id}: {decision} ({reason})")


def update_review_decision_reviewer(ticket_id: str, reviewer: str) -> None:
    """
    Update the most recent log entry with assigned reviewer

    Args:
        ticket_id: JIRA ticket ID to update
        reviewer: Reviewer name to assign

    Note:
        For large CSV files (>10k rows), consider using a database instead.
        Current implementation loads entire file into memory for simplicity.
    """
    module_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(module_dir, '..', 'metrics', 'review-decisions.csv')
    log_path = os.path.normpath(log_path)

    if not os.path.exists(log_path):
        logging.warning(f"Cannot update reviewer: log file not found at {log_path}")
        return

    # Read all rows
    with open(log_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Find and update the most recent entry for this ticket
    updated = False
    for row in reversed(rows):
        if row['ticket_id'] == ticket_id:
            row['reviewer'] = reviewer
            updated = True
            break

    if not updated:
        logging.warning(f"No decision log entry found for ticket {ticket_id}")
        return

    # Write back
    with open(log_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['ticket_id', 'priority', 'review_decision', 'reason', 'timestamp', 'reviewer'])
        writer.writeheader()
        writer.writerows(rows)
