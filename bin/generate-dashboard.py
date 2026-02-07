#!/usr/bin/env python3
"""
WXCODE Dashboard Generator

Generates deterministic JSON dashboards from .planning/ files.
Usage: python generate-dashboard.py [--all] [--project-dir PATH]

Outputs:
  - .planning/dashboard.json (project dashboard)
  - .planning/dashboard_<milestone>.json (milestone dashboards, with --all)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import xml.etree.ElementTree as ET


def parse_args():
    parser = argparse.ArgumentParser(description="Generate WXCODE dashboards")
    parser.add_argument("--all", action="store_true", help="Regenerate all milestone dashboards")
    parser.add_argument("--project-dir", type=str, default=".", help="Project directory path")
    parser.add_argument("--wxcode-version", type=str, default=None, help="WXCODE version")
    return parser.parse_args()


def get_wxcode_version(provided_version: Optional[str] = None) -> str:
    """Get WXCODE version from VERSION file or provided value."""
    if provided_version:
        return provided_version

    version_paths = [
        Path.home() / ".claude" / "wxcode-skill" / "VERSION",
        Path(__file__).parent.parent / "VERSION",
    ]

    for path in version_paths:
        if path.exists():
            return path.read_text().strip()

    return "unknown"


def parse_markdown_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown file."""
    frontmatter = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return frontmatter


def extract_xml_tasks(content: str) -> list:
    """Extract tasks from XML <task> blocks in PLAN.md content."""
    tasks = []

    # Find all <task> blocks
    task_pattern = r'<task[^>]*>(.*?)</task>'
    matches = re.findall(task_pattern, content, re.DOTALL)

    for i, match in enumerate(matches, 1):
        task = {"sequence": i}

        # Extract name
        name_match = re.search(r'<name>(.*?)</name>', match, re.DOTALL)
        if name_match:
            name = name_match.group(1).strip()
            # Remove "Task N: " prefix if present
            name = re.sub(r'^Task\s+\d+:\s*', '', name)
            task["name"] = name

        # Extract files
        files_match = re.search(r'<files>(.*?)</files>', match, re.DOTALL)
        if files_match:
            files = files_match.group(1).strip()
            # Take first file if comma-separated
            task["file"] = files.split(",")[0].strip()

        # Extract action (description)
        action_match = re.search(r'<action>(.*?)</action>', match, re.DOTALL)
        if action_match:
            action = action_match.group(1).strip()
            # Take first line or first 100 chars
            first_line = action.split("\n")[0].strip()
            task["description"] = first_line[:200] if len(first_line) > 200 else first_line

        tasks.append(task)

    return tasks


def detect_phases_dir(planning_dir: Path, milestone_folder: Optional[Path] = None) -> Optional[Path]:
    """Detect phases directory (nested or flat structure).

    Handles multiple structures:
    1. Nested: milestone_folder/phases/ (e.g., .planning/v1.0-PAGE_Login/phases/)
    2. Flat: planning_dir/phases/ (e.g., .planning/phases/)
    3. Marker folder: milestones/v1.0-PAGE_Login/ is empty, phases in .planning/phases/
    """
    # Check nested structure first
    if milestone_folder and (milestone_folder / "phases").is_dir():
        phases_dir = milestone_folder / "phases"
        # Verify it has actual phase directories
        phase_dirs = [d for d in phases_dir.iterdir() if d.is_dir() and re.match(r'\d+-', d.name)]
        if phase_dirs:
            return phases_dir

    # Fall back to flat structure (.planning/phases/)
    if (planning_dir / "phases").is_dir():
        return planning_dir / "phases"

    return None


def parse_plan_file(plan_path: Path) -> dict:
    """Parse a PLAN.md file and extract plan info with tasks."""
    content = plan_path.read_text()
    frontmatter = parse_markdown_frontmatter(content)

    # Extract plan number from filename (e.g., 01-01-PLAN.md -> "1.1")
    filename = plan_path.name
    match = re.match(r'(\d+)-(\d+)-PLAN\.md', filename)
    if match:
        phase_num = int(match.group(1))
        plan_num = int(match.group(2))
        plan_number = f"{phase_num}.{plan_num}"
    else:
        plan_number = "1.1"

    # Extract plan name from objective or frontmatter
    name = frontmatter.get("name", "")
    if not name:
        objective_match = re.search(r'<objective>\s*(.*?)\n', content, re.DOTALL)
        if objective_match:
            name = objective_match.group(1).strip()[:100]
        else:
            name = plan_path.parent.name.replace("-", " ").title()

    # Check if SUMMARY.md exists
    summary_name = filename.replace("-PLAN.md", "-SUMMARY.md")
    summary_path = plan_path.parent / summary_name
    status = "complete" if summary_path.exists() else "pending"

    # Extract summary content if exists
    summary_text = None
    if summary_path.exists():
        summary_content = summary_path.read_text()
        # Try to get first paragraph after frontmatter
        summary_match = re.search(r'---.*?---\s*(.+?)(?:\n\n|\n#)', summary_content, re.DOTALL)
        if summary_match:
            summary_text = summary_match.group(1).strip()[:200]

    # Extract tasks
    tasks = extract_xml_tasks(content)

    # Build task objects with proper IDs
    task_objects = []
    for task in tasks:
        task_id = f"{plan_number}.{task['sequence']}"
        task_objects.append({
            "id": task_id,
            "name": task.get("name", f"Task {task['sequence']}"),
            "file": task.get("file"),
            "status": status,  # Task status follows plan status
            "description": task.get("description", "")
        })

    return {
        "number": plan_number,
        "name": name,
        "status": status,
        "summary": summary_text,
        "tasks": task_objects
    }


def parse_phase_directory(phase_dir: Path) -> dict:
    """Parse a phase directory and extract all plans."""
    # Extract phase number and name from directory name (e.g., 01-database-model)
    dir_name = phase_dir.name
    match = re.match(r'(\d+)-(.+)', dir_name)
    if match:
        phase_num = int(match.group(1))
        phase_name = match.group(2).replace("-", " ").title()
    else:
        phase_num = 1
        phase_name = dir_name

    # Find all PLAN.md files
    plan_files = sorted(phase_dir.glob("*-PLAN.md"))
    plans = [parse_plan_file(pf) for pf in plan_files]

    # Determine phase status
    if not plans:
        status = "pending"
    elif all(p["status"] == "complete" for p in plans):
        status = "complete"
    elif any(p["status"] == "complete" for p in plans):
        status = "in_progress"
    else:
        status = "pending"

    # Check for verification
    verification_files = list(phase_dir.glob("*-VERIFICATION.md"))
    verified = len(verification_files) > 0

    return {
        "number": phase_num,
        "name": phase_name,
        "goal": "",  # Will be populated from ROADMAP.md
        "status": status,
        "requirements_covered": [],  # Will be populated from ROADMAP.md
        "plans": plans,
        "verified": verified
    }


def parse_roadmap(roadmap_path: Path) -> dict:
    """Parse ROADMAP.md to extract phase goals and requirements."""
    if not roadmap_path.exists():
        return {}

    content = roadmap_path.read_text()
    phases_info = {}

    # Find phase sections: ### Phase N: Name
    phase_pattern = r'###\s*Phase\s+(\d+):\s*([^\n]+)'
    matches = re.finditer(phase_pattern, content)

    for match in matches:
        phase_num = int(match.group(1))
        phase_name = match.group(2).strip()

        # Get content until next phase or section
        start = match.end()
        next_phase = re.search(r'\n###\s*Phase\s+\d+:', content[start:])
        next_section = re.search(r'\n##\s+', content[start:])

        if next_phase and next_section:
            end = start + min(next_phase.start(), next_section.start())
        elif next_phase:
            end = start + next_phase.start()
        elif next_section:
            end = start + next_section.start()
        else:
            end = len(content)

        section_content = content[start:end]

        # Extract goal
        goal_match = re.search(r'\*\*Goal:\*\*\s*([^\n]+)', section_content)
        goal = goal_match.group(1).strip() if goal_match else ""

        # Extract requirements
        req_pattern = r'([A-Z]+-\d+)'
        requirements = re.findall(req_pattern, section_content)

        phases_info[phase_num] = {
            "name": phase_name,
            "goal": goal,
            "requirements": list(set(requirements))
        }

    return phases_info


def parse_requirements(requirements_path: Path) -> dict:
    """Parse REQUIREMENTS.md to get requirement completion status."""
    if not requirements_path.exists():
        return {"total": 0, "complete": 0, "by_category": {}}

    content = requirements_path.read_text()

    total = 0
    complete = 0
    by_category = {}

    # Find requirements: - [x] **REQ-01**: Description or - [ ] **REQ-01**: Description
    req_pattern = r'-\s*\[([ xX])\]\s*\*\*([A-Z]+)-(\d+)\*\*'
    matches = re.finditer(req_pattern, content)

    for match in matches:
        is_complete = match.group(1).lower() == 'x'
        category = match.group(2)

        total += 1
        if is_complete:
            complete += 1

        if category not in by_category:
            by_category[category] = {"total": 0, "complete": 0}

        by_category[category]["total"] += 1
        if is_complete:
            by_category[category]["complete"] += 1

    return {
        "total": total,
        "complete": complete,
        "by_category": by_category
    }


def detect_workflow_stages(
    planning_dir: Path,
    phases_dir: Optional[Path],
    phases: list,
    is_archived: bool = False,
    milestone_name: str = ""
) -> dict:
    """Detect workflow stage status.

    Args:
        planning_dir: The directory to check for files
        phases_dir: The phases directory
        phases: List of parsed phases
        is_archived: Whether this is an archived milestone
        milestone_name: Name like "v1.0-PAGE_Login" for finding archived files
    """
    now = datetime.now().isoformat() + "Z"

    stages = [
        {"id": "created", "name": "Milestone Created", "status": "pending", "completed_at": None},
        {"id": "requirements", "name": "Requirements Defined", "status": "pending", "completed_at": None},
        {"id": "roadmap", "name": "Roadmap Created", "status": "pending", "completed_at": None},
        {"id": "planning", "name": "All Phases Planned", "status": "pending", "completed_at": None},
        {"id": "executing", "name": "Execution In Progress", "status": "pending", "completed_at": None},
        {"id": "verified", "name": "Work Verified", "status": "pending", "completed_at": None},
        {"id": "archived", "name": "Milestone Archived", "status": "pending", "completed_at": None},
    ]

    # For archived milestones, all stages are complete by definition
    if is_archived:
        for stage in stages:
            stage["status"] = "complete"
            stage["completed_at"] = now
        return {
            "current_stage": "archived",
            "stages": stages
        }

    # Check created (folder exists)
    if planning_dir.exists():
        stages[0]["status"] = "complete"
        stages[0]["completed_at"] = datetime.fromtimestamp(planning_dir.stat().st_ctime).isoformat() + "Z"

    # Check requirements - try multiple locations
    req_paths = [
        planning_dir / "REQUIREMENTS.md",
    ]
    for req_path in req_paths:
        if req_path.exists() and req_path.stat().st_size > 100:
            stages[1]["status"] = "complete"
            stages[1]["completed_at"] = datetime.fromtimestamp(req_path.stat().st_mtime).isoformat() + "Z"
            break

    # Check roadmap - try multiple locations
    roadmap_paths = [
        planning_dir / "ROADMAP.md",
    ]
    for roadmap_path in roadmap_paths:
        if roadmap_path.exists() and roadmap_path.stat().st_size > 100:
            stages[2]["status"] = "complete"
            stages[2]["completed_at"] = datetime.fromtimestamp(roadmap_path.stat().st_mtime).isoformat() + "Z"
            break

    # Check planning (all phases have at least one PLAN.md)
    if phases:
        phases_with_plans = sum(1 for p in phases if p.get("plans"))
        if phases_with_plans == len(phases):
            stages[3]["status"] = "complete"
        elif phases_with_plans > 0:
            stages[3]["status"] = "in_progress"

    # Check executing (phases with SUMMARY.md)
    if phases:
        phases_complete = sum(1 for p in phases if p.get("status") == "complete")
        if phases_complete == len(phases):
            stages[4]["status"] = "complete"
        elif phases_complete > 0:
            stages[4]["status"] = "in_progress"

    # Check verified - look for UAT files in phases or planning dir
    verified = False
    if phases_dir and phases_dir.exists():
        uat_files = list(phases_dir.glob("**/*-UAT.md"))
        for uat_file in uat_files:
            uat_content = uat_file.read_text().lower()
            if "status: complete" in uat_content:
                verified = True
                break

    # Also check for phase verification markers
    if not verified and phases:
        verified = all(p.get("verified", False) for p in phases)

    if verified:
        stages[5]["status"] = "complete"

    # Determine current stage
    current_stage = "created"
    for stage in stages:
        if stage["status"] == "in_progress":
            current_stage = stage["id"]
            break
        elif stage["status"] == "pending":
            current_stage = stage["id"]
            break

    return {
        "current_stage": current_stage,
        "stages": stages
    }


def calculate_progress(phases: list, requirements: dict) -> dict:
    """Calculate progress statistics."""
    phases_total = len(phases)
    phases_complete = sum(1 for p in phases if p.get("status") == "complete")

    plans_total = sum(len(p.get("plans", [])) for p in phases)
    plans_complete = sum(
        sum(1 for pl in p.get("plans", []) if pl.get("status") == "complete")
        for p in phases
    )

    tasks_total = sum(
        sum(len(pl.get("tasks", [])) for pl in p.get("plans", []))
        for p in phases
    )
    tasks_complete = sum(
        sum(
            sum(1 for t in pl.get("tasks", []) if t.get("status") == "complete")
            for pl in p.get("plans", [])
        )
        for p in phases
    )

    return {
        "phases_complete": phases_complete,
        "phases_total": phases_total,
        "phases_percentage": round((phases_complete / phases_total * 100) if phases_total else 0),
        "plans_complete": plans_complete,
        "plans_total": plans_total,
        "plans_percentage": round((plans_complete / plans_total * 100) if plans_total else 0),
        "tasks_complete": tasks_complete,
        "tasks_total": tasks_total,
        "tasks_percentage": round((tasks_complete / tasks_total * 100) if tasks_total else 0),
        "requirements_complete": requirements.get("complete", 0),
        "requirements_total": requirements.get("total", 0),
        "requirements_percentage": round(
            (requirements.get("complete", 0) / requirements.get("total", 1) * 100)
            if requirements.get("total", 0) else 0
        )
    }


def generate_milestone_dashboard(
    planning_dir: Path,
    milestone_name: str,
    wxcode_version: str,
    root_planning_dir: Optional[Path] = None,
    is_archived: bool = False
) -> dict:
    """Generate a complete milestone dashboard.

    Args:
        planning_dir: The milestone folder path (could be .planning or .planning/milestones/v1.0-X)
        milestone_name: Name of the milestone (e.g., v1.0-PAGE_Login)
        wxcode_version: WXCODE version string
        root_planning_dir: The root .planning directory (for fallback phases lookup)
        is_archived: Whether this milestone is archived
    """

    # Parse milestone info from folder name
    match = re.match(r'(v[\d.]+)-(.+)', milestone_name)
    if match:
        version = match.group(1)
        element = match.group(2)
    else:
        version = "v1.0"
        element = milestone_name

    # Use root_planning_dir for fallback if provided
    if root_planning_dir is None:
        root_planning_dir = planning_dir

    # Detect phases directory (check milestone folder first, then root)
    phases_dir = detect_phases_dir(root_planning_dir, planning_dir)

    # Parse all phases
    phases = []
    if phases_dir and phases_dir.exists():
        phase_dirs = sorted([d for d in phases_dir.iterdir() if d.is_dir() and re.match(r'\d+-', d.name)])
        phases = [parse_phase_directory(pd) for pd in phase_dirs]

    # For archived milestones, files may be prefixed with version (e.g., v1.0-REQUIREMENTS.md)
    # in the milestones/ directory
    milestones_dir = root_planning_dir / "milestones" if root_planning_dir else None

    # Parse roadmap for goals and requirements
    roadmap_path = None
    roadmap_candidates = [
        planning_dir / "ROADMAP.md",
    ]
    if root_planning_dir:
        roadmap_candidates.append(root_planning_dir / "ROADMAP.md")
    if milestones_dir and milestones_dir.exists():
        # Archived milestones use version-prefixed files
        roadmap_candidates.append(milestones_dir / f"{version}-ROADMAP.md")

    for candidate in roadmap_candidates:
        if candidate.exists():
            roadmap_path = candidate
            break

    roadmap_info = parse_roadmap(roadmap_path) if roadmap_path else {}

    # Enrich phases with roadmap info
    for phase in phases:
        phase_num = phase["number"]
        if phase_num in roadmap_info:
            phase["goal"] = roadmap_info[phase_num].get("goal", "")
            phase["requirements_covered"] = roadmap_info[phase_num].get("requirements", [])

    # Parse requirements - check multiple locations
    requirements_path = None
    req_candidates = [
        planning_dir / "REQUIREMENTS.md",
    ]
    if root_planning_dir:
        req_candidates.append(root_planning_dir / "REQUIREMENTS.md")
    if milestones_dir and milestones_dir.exists():
        # Archived milestones use version-prefixed files
        req_candidates.append(milestones_dir / f"{version}-REQUIREMENTS.md")

    for candidate in req_candidates:
        if candidate.exists():
            requirements_path = candidate
            break

    requirements = parse_requirements(requirements_path) if requirements_path else {"total": 0, "complete": 0, "by_category": {}}

    # Detect workflow stages
    workflow = detect_workflow_stages(
        root_planning_dir or planning_dir,
        phases_dir,
        phases,
        is_archived=is_archived,
        milestone_name=milestone_name
    )

    # For archived milestones, mark all requirements as complete
    if is_archived and requirements.get("total", 0) > 0:
        requirements["complete"] = requirements["total"]
        for cat in requirements.get("by_category", {}).values():
            cat["complete"] = cat["total"]

    # Calculate progress
    progress = calculate_progress(phases, requirements)

    # For archived milestones, ensure all progress is 100%
    if is_archived:
        if progress["phases_total"] > 0:
            progress["phases_complete"] = progress["phases_total"]
            progress["phases_percentage"] = 100
        if progress["plans_total"] > 0:
            progress["plans_complete"] = progress["plans_total"]
            progress["plans_percentage"] = 100
        if progress["tasks_total"] > 0:
            progress["tasks_complete"] = progress["tasks_total"]
            progress["tasks_percentage"] = 100
        if progress["requirements_total"] > 0:
            progress["requirements_complete"] = progress["requirements_total"]
            progress["requirements_percentage"] = 100

    # Determine current position
    current_phase = None
    current_plan = None
    if not is_archived:
        for phase in phases:
            if phase["status"] != "complete":
                current_phase = phase["number"]
                for plan in phase.get("plans", []):
                    if plan["status"] != "complete":
                        current_plan = plan["number"]
                        break
                break

    # Determine milestone status
    if is_archived:
        milestone_status = "completed"
    elif any(p["status"] != "complete" for p in phases):
        milestone_status = "in_progress"
    else:
        milestone_status = "completed"

    # Build dashboard
    dashboard = {
        "milestone": {
            "folder_name": milestone_name,
            "mongodb_id": None,  # Would need MCP to get this
            "wxcode_version": version,
            "element_name": element,
            "status": milestone_status,
            "created_at": datetime.now().isoformat() + "Z",
            "completed_at": datetime.now().isoformat() + "Z" if is_archived else None
        },
        "workflow": workflow,
        "current_position": {
            "phase_number": current_phase,
            "phase_name": next((p["name"] for p in phases if p["number"] == current_phase), None),
            "plan_number": current_plan,
            "plan_total": progress["plans_total"],
            "status": "complete" if is_archived or not current_phase else "in_progress"
        },
        "progress": progress,
        "phases": phases,
        "requirements": requirements,
        "blockers": [],
        "meta": {
            "generated_at": datetime.now().isoformat() + "Z",
            "wxcode_version": wxcode_version,
            "generator": "generate-dashboard.py"
        }
    }

    return dashboard


def parse_project_md(project_path: Path) -> dict:
    """Parse PROJECT.md for project info."""
    if not project_path.exists():
        return {}

    content = project_path.read_text()

    # Extract name (first H1)
    name_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else "Unknown Project"

    # Extract core value
    core_value_match = re.search(r'##\s*Core Value\s*\n+(.+?)(?=\n#|\Z)', content, re.DOTALL)
    core_value = core_value_match.group(1).strip() if core_value_match else ""

    # Extract description
    desc_match = re.search(r'##\s*What This Is\s*\n+(.+?)(?=\n#|\Z)', content, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else ""

    return {
        "name": name,
        "core_value": core_value[:500] if core_value else "",
        "description": description[:500] if description else ""
    }


def parse_conversion_md(conversion_path: Path) -> dict:
    """Parse CONVERSION.md for conversion project info."""
    if not conversion_path.exists():
        return {"is_conversion_project": False}

    content = conversion_path.read_text()

    # Extract stack
    stack_match = re.search(r'stack[:\s]+([a-z0-9-]+)', content, re.IGNORECASE)
    stack = stack_match.group(1) if stack_match else None

    return {
        "is_conversion_project": True,
        "stack": stack
    }


def find_milestones(planning_dir: Path) -> list:
    """Find all milestone folders."""
    milestones = []

    # Check for nested milestone folders (.planning/v1.0-PAGE_Login/)
    for item in planning_dir.iterdir():
        if item.is_dir() and re.match(r'v[\d.]+-', item.name):
            milestones.append({
                "folder_name": item.name,
                "path": item,
                "archived": False
            })

    # Check for archived milestones (.planning/milestones/v1.0-PAGE_Login/)
    milestones_dir = planning_dir / "milestones"
    if milestones_dir.exists():
        for item in milestones_dir.iterdir():
            if item.is_dir() and re.match(r'v[\d.]+-', item.name):
                milestones.append({
                    "folder_name": item.name,
                    "path": item,
                    "archived": True
                })

    # Check for flat structure (single active milestone)
    if not milestones and (planning_dir / "ROADMAP.md").exists():
        # Try to get milestone name from STATE.md
        state_path = planning_dir / "STATE.md"
        milestone_name = "v1.0-current"
        if state_path.exists():
            content = state_path.read_text()
            match = re.search(r'Milestone:\s*(v[\d.]+-[^\s\n]+)', content)
            if match:
                milestone_name = match.group(1)

        milestones.append({
            "folder_name": milestone_name,
            "path": planning_dir,
            "archived": False
        })

    return milestones


def generate_project_dashboard(
    planning_dir: Path,
    milestones: list,
    wxcode_version: str
) -> dict:
    """Generate the project dashboard."""

    # Parse project info
    project_info = parse_project_md(planning_dir / "PROJECT.md")

    # Parse conversion info
    conversion_info = parse_conversion_md(planning_dir / "CONVERSION.md")

    # Build milestones array
    milestones_array = []
    for m in milestones:
        match = re.match(r'(v[\d.]+)-(.+)', m["folder_name"])
        if match:
            version = match.group(1)
            element = match.group(2)
        else:
            version = "v1.0"
            element = m["folder_name"]

        milestones_array.append({
            "folder_name": m["folder_name"],
            "mongodb_id": None,
            "wxcode_version": version,
            "element_name": element,
            "status": "completed" if m["archived"] else "in_progress",
            "created_at": datetime.now().isoformat() + "Z",
            "completed_at": None
        })

    # Find current milestone
    current_milestone = next(
        (m["folder_name"] for m in milestones if not m["archived"]),
        milestones[0]["folder_name"] if milestones else None
    )

    # Calculate progress
    milestones_complete = sum(1 for m in milestones if m["archived"])
    milestones_total = len(milestones)

    return {
        "project": project_info,
        "conversion": {
            "is_conversion_project": conversion_info.get("is_conversion_project", False),
            "elements_converted": None,  # Would need MCP
            "elements_total": None,  # Would need MCP
            "stack": conversion_info.get("stack")
        },
        "milestones": milestones_array,
        "current_milestone": current_milestone,
        "progress": {
            "milestones_complete": milestones_complete,
            "milestones_total": milestones_total,
            "milestones_percentage": round((milestones_complete / milestones_total * 100) if milestones_total else 0)
        },
        "meta": {
            "generated_at": datetime.now().isoformat() + "Z",
            "wxcode_version": wxcode_version,
            "generator": "generate-dashboard.py"
        }
    }


def main():
    args = parse_args()

    project_dir = Path(args.project_dir).resolve()
    planning_dir = project_dir / ".planning"

    if not planning_dir.exists():
        print(f"ERROR: No .planning directory found in {project_dir}", file=sys.stderr)
        sys.exit(1)

    wxcode_version = get_wxcode_version(args.wxcode_version)

    # Find all milestones
    milestones = find_milestones(planning_dir)

    if not milestones:
        print("ERROR: No milestones found", file=sys.stderr)
        sys.exit(1)

    # Generate project dashboard
    project_dashboard = generate_project_dashboard(planning_dir, milestones, wxcode_version)

    project_dashboard_path = planning_dir / "dashboard.json"
    project_dashboard_path.write_text(json.dumps(project_dashboard, indent=2, ensure_ascii=False))
    print(f"[WXCODE:DASHBOARD_UPDATED] {project_dashboard_path}")

    # Generate milestone dashboards if --all
    if args.all:
        for milestone in milestones:
            milestone_dashboard = generate_milestone_dashboard(
                milestone["path"],
                milestone["folder_name"],
                wxcode_version,
                root_planning_dir=planning_dir,  # Pass root for fallback phases lookup
                is_archived=milestone["archived"]
            )

            dashboard_filename = f"dashboard_{milestone['folder_name']}.json"
            dashboard_path = planning_dir / dashboard_filename
            dashboard_path.write_text(json.dumps(milestone_dashboard, indent=2, ensure_ascii=False))
            print(f"[WXCODE:DASHBOARD_UPDATED] {dashboard_path}")

    print(f"\nDashboards generated successfully (WXCODE {wxcode_version})")


if __name__ == "__main__":
    main()
