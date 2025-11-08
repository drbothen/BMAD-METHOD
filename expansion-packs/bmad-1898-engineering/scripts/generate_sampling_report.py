#!/usr/bin/env python3
"""
Generate sampling statistics report from review-decisions.csv
Story 3.4: Priority-Based Review Triggering

Usage: python scripts/generate_sampling_report.py [--month YYYY-MM]
"""

import csv
import argparse
import os
from collections import defaultdict
from datetime import datetime


def generate_report(log_path, month=None):
    """
    Generate sampling statistics report

    Args:
        log_path: Path to review-decisions.csv
        month: Optional month filter (YYYY-MM format)

    Returns:
        str: Markdown-formatted report
    """
    if not os.path.exists(log_path):
        return f"# Error: Log file not found at {log_path}\n\nNo review decisions have been logged yet."

    # Read review decisions
    with open(log_path, 'r') as f:
        reader = csv.DictReader(f)
        decisions = list(reader)

    if not decisions:
        return "# Error: No review decisions found\n\nThe log file exists but contains no data."

    # Filter by month if specified
    if month:
        decisions = [d for d in decisions if d['timestamp'].startswith(month)]
        if not decisions:
            return f"# Error: No data for {month}\n\nNo review decisions found for the specified month."

    # Calculate statistics by priority
    stats = defaultdict(lambda: {'total': 0, 'mandatory': 0, 'sampled': 0, 'skipped': 0})

    for decision in decisions:
        priority = decision['priority']
        stats[priority]['total'] += 1

        if decision['review_decision'] == 'required':
            if 'Mandatory' in decision['reason']:
                stats[priority]['mandatory'] += 1
            else:
                stats[priority]['sampled'] += 1
        else:
            stats[priority]['skipped'] += 1

    # Generate markdown report
    total_tickets = sum(s['total'] for s in stats.values())
    total_reviewed = sum(s['mandatory'] + s['sampled'] for s in stats.values())
    total_skipped = sum(s['skipped'] for s in stats.values())

    report = f"# Review Sampling Statistics - {month or 'All Time'}\n\n"
    report += "## Overall\n\n"
    report += f"- Total Tickets: {total_tickets}\n"
    report += f"- Reviewed: {total_reviewed} ({total_reviewed/total_tickets*100:.1f}%)\n"
    report += f"- Skipped: {total_skipped} ({total_skipped/total_tickets*100:.1f}%)\n\n"
    report += "## By Priority\n\n"
    report += "| Priority | Total | Mandatory | Sampled | Skipped | Review Rate |\n"
    report += "| -------- | ----- | --------- | ------- | ------- | ----------- |\n"

    for priority in ['P1', 'P2', 'P3', 'P4', 'P5']:
        s = stats[priority]
        if s['total'] > 0:
            review_rate = (s['mandatory'] + s['sampled']) / s['total'] * 100
            report += f"| {priority} | {s['total']} | {s['mandatory']} ({s['mandatory']/s['total']*100:.0f}%) | "
            report += f"{s['sampled']} ({s['sampled']/s['total']*100:.0f}%) | {s['skipped']} | {review_rate:.0f}% |\n"

    report += "\n## Target Compliance\n\n"

    # Check compliance with targets
    targets = {'P1': 100, 'P2': 100, 'P3': 25, 'P4': 10, 'P5': 5}
    for priority, target in targets.items():
        s = stats[priority]
        if s['total'] > 0:
            actual = (s['mandatory'] + s['sampled']) / s['total'] * 100
            # Allow ±5% tolerance for statistical variance
            status = '✅' if abs(actual - target) <= 5 else '⚠️'
            report += f"- {priority}: Target {target}%, Actual {actual:.0f}% {status}\n"
        else:
            report += f"- {priority}: Target {target}%, Actual N/A ⚠️ (no data)\n"

    # Add detailed decision log
    report += "\n## Recent Decisions (Last 10)\n\n"
    report += "| Timestamp | Ticket ID | Priority | Decision | Reason | Reviewer |\n"
    report += "| --------- | --------- | -------- | -------- | ------ | -------- |\n"

    # Show last 10 decisions
    for decision in decisions[-10:]:
        timestamp = decision['timestamp'][:19]  # Trim to just datetime
        report += f"| {timestamp} | {decision['ticket_id']} | {decision['priority']} | "
        report += f"{decision['review_decision']} | {decision['reason'][:40]}... | {decision['reviewer']} |\n"

    return report


def main():
    """Main entry point for CLI usage"""
    parser = argparse.ArgumentParser(description='Generate review sampling statistics report')
    parser.add_argument('--month', help='Filter by month (YYYY-MM format)')
    parser.add_argument('--output', help='Output file path (optional, prints to stdout if not specified)')
    args = parser.parse_args()

    # Get path relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, '..', 'metrics', 'review-decisions.csv')
    log_path = os.path.normpath(log_path)

    report = generate_report(log_path, args.month)

    # Print to stdout
    print(report)

    # Optionally save to file
    if args.output:
        output_path = args.output
    elif args.month:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, '..', 'metrics', f'sampling-report-{args.month}.md')
        output_path = os.path.normpath(output_path)
    else:
        output_path = None

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"\nReport saved to: {output_path}")


if __name__ == '__main__':
    main()
