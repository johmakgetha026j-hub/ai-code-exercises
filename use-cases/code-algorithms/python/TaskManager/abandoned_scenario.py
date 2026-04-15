"""
Scenario: Demonstrate the abandoned task business rule

Business Rule:
"Tasks that are overdue for more than 7 days should be automatically 
marked as abandoned unless they are marked as high priority."

This script shows how the system handles this rule in different cases.
"""

from datetime import datetime, timedelta
from models import Task, TaskPriority, TaskStatus
from task_manager import TaskManager

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_task_info(task):
    """Helper to print task details."""
    days_overdue = (datetime.now() - task.due_date).days if task.due_date else "N/A"
    abandoned_status = "ABANDONED" if task.is_abandoned() else "ACTIVE"
    
    print(f"  ID: {task.id[:8]}")
    print(f"  Title: {task.title}")
    print(f"  Priority: {task.priority.name}")
    print(f"  Status: {task.status.value}")
    print(f"  Due Date: {task.due_date.strftime('%Y-%m-%d') if task.due_date else 'None'}")
    print(f"  Days Overdue: {days_overdue}")
    print(f"  Task Status: {abandoned_status}")
    print(f"  Tags: {', '.join(task.tags) if task.tags else 'None'}")
    print()

def main():
    print_section("ABANDONED TASK BUSINESS RULE DEMONSTRATION")
    
    # Create a TaskManager with a test storage file
    tm = TaskManager(storage_path="scenario_test_tasks.json")
    
    # Clear any existing test data
    for task in tm.storage.get_all_tasks():
        tm.delete_task(task.id)
    
    print("SCENARIO SETUP:")
    print("Creating sample tasks to demonstrate the abandoned rule...\n")
    
    # Task 1: LOW priority, overdue by 10 days → SHOULD BE ABANDONED
    print("1. Creating LOW priority task overdue by 10 days...")
    due_date_1 = datetime.now() - timedelta(days=10)
    task_id_1 = tm.create_task(
        title="Low Priority Overdue Task",
        description="This task is low priority and overdue for 10 days",
        priority_value=TaskPriority.LOW.value,
        due_date_str=due_date_1.strftime('%Y-%m-%d'),
        tags=["review"]
    )
    print(f"   Created task: {task_id_1[:8]}\n")
    
    # Task 2: HIGH priority, overdue by 10 days → SHOULD NOT BE ABANDONED
    print("2. Creating HIGH priority task overdue by 10 days...")
    due_date_2 = datetime.now() - timedelta(days=10)
    task_id_2 = tm.create_task(
        title="High Priority Overdue Task",
        description="This task is high priority and overdue for 10 days",
        priority_value=TaskPriority.HIGH.value,
        due_date_str=due_date_2.strftime('%Y-%m-%d'),
        tags=["critical"]
    )
    print(f"   Created task: {task_id_2[:8]}\n")
    
    # Task 3: MEDIUM priority, overdue by 5 days → SHOULD NOT BE ABANDONED (< 7 days)
    print("3. Creating MEDIUM priority task overdue by 5 days...")
    due_date_3 = datetime.now() - timedelta(days=5)
    task_id_3 = tm.create_task(
        title="Medium Priority Slightly Overdue Task",
        description="This task is medium priority, only 5 days overdue",
        priority_value=TaskPriority.MEDIUM.value,
        due_date_str=due_date_3.strftime('%Y-%m-%d'),
        tags=["standard"]
    )
    print(f"   Created task: {task_id_3[:8]}\n")
    
    # Task 4: URGENT priority, overdue by 15 days → SHOULD NOT BE ABANDONED (HIGH PRIORITY)
    print("4. Creating URGENT priority task overdue by 15 days...")
    due_date_4 = datetime.now() - timedelta(days=15)
    task_id_4 = tm.create_task(
        title="Urgent Priority Task",
        description="This task is urgent and overdue for 15 days",
        priority_value=TaskPriority.URGENT.value,
        due_date_str=due_date_4.strftime('%Y-%m-%d'),
        tags=["blocker"]
    )
    print(f"   Created task: {task_id_4[:8]}\n")
    
    # Task 5: MEDIUM priority, completed → SHOULD NOT BE ABANDONED (DONE)
    print("5. Creating completed MEDIUM priority task overdue by 10 days...")
    due_date_5 = datetime.now() - timedelta(days=10)
    task_id_5 = tm.create_task(
        title="Completed Overdue Task",
        description="This task was already completed",
        priority_value=TaskPriority.MEDIUM.value,
        due_date_str=due_date_5.strftime('%Y-%m-%d'),
        tags=[]
    )
    tm.update_task_status(task_id_5, "done")
    print(f"   Created and completed task: {task_id_5[:8]}\n")
    
    # ANALYSIS SECTION
    print_section("ANALYSIS: CHECKING ABANDONED RULE")
    
    print("Business Rule Check:")
    print("  Conditions for ABANDONMENT:")
    print("  ✓ Task is overdue (due_date < now)")
    print("  ✓ Task is overdue for MORE THAN 7 days") 
    print("  ✓ Task priority is NOT HIGH or URGENT")
    print("  ✓ Task status is NOT DONE\n")
    
    # Get all tasks
    all_tasks = tm.storage.get_all_tasks()
    
    print(f"Total tasks created: {len(all_tasks)}\n")
    
    # Check each task
    print("Individual Task Evaluation:")
    print("-" * 60)
    for task in all_tasks:
        print(f"\nTask: {task.title}")
        print_task_info(task)
        
        # Explain the rule evaluation
        days_overdue = (datetime.now() - task.due_date).days if task.due_date else 0
        is_high_priority = task.priority in (TaskPriority.HIGH, TaskPriority.URGENT)
        
        print("  Evaluation:")
        print(f"    - Is overdue: {task.is_overdue()}")
        print(f"    - Days overdue: {days_overdue}")
        print(f"    - Overdue > 7 days: {days_overdue > 7}")
        print(f"    - Is HIGH or URGENT priority: {is_high_priority}")
        print(f"    - Status is DONE: {task.status == TaskStatus.DONE}")
        print(f"    → Should be ABANDONED: {task.is_abandoned()}")
    
    # SUMMARY SECTION
    print_section("SUMMARY: ABANDONED TASKS REPORT")
    
    abandoned_tasks = tm.get_abandoned_tasks()
    print(f"Tasks meeting abandonment criteria: {len(abandoned_tasks)}")
    
    if abandoned_tasks:
        print("\nTasks that should be marked as ABANDONED:\n")
        for task in abandoned_tasks:
            print(f"  • {task.title}")
            print(f"    (Priority: {task.priority.name}, Overdue: {(datetime.now() - task.due_date).days} days)\n")
    else:
        print("No tasks meet the abandonment criteria.\n")
    
    # AUTOMATIC MARKING
    print_section("AUTOMATIC MARKING: APPLYING BUSINESS RULE")
    
    print("Applying mark_abandoned_tasks() to tag abandoned tasks...\n")
    marked_count = tm.mark_abandoned_tasks()
    
    print(f"Tasks marked as abandoned: {marked_count}\n")
    
    print("Updated task tags:")
    print("-" * 60)
    for task in tm.storage.get_all_tasks():
        if "abandoned" in task.tags:
            print(f"✗ {task.title}")
            print(f"  Tags: {', '.join(task.tags)}\n")
    
    # STATISTICS
    print_section("STATISTICS: DASHBOARD VIEW")
    
    stats = tm.get_statistics()
    
    print(f"Total tasks: {stats['total']}")
    print(f"Overdue tasks: {stats['overdue']}")
    print(f"Abandoned tasks: {stats['abandoned']}")
    print(f"\nStatus breakdown:")
    for status, count in stats['by_status'].items():
        print(f"  {status}: {count}")
    print(f"\nPriority breakdown:")
    for priority, count in stats['by_priority'].items():
        print(f"  {priority}: {count}")
    
    # Cleanup
    print_section("CLEANUP")
    print("Test scenario complete. Cleaning up test data...")
    for task in tm.storage.get_all_tasks():
        tm.delete_task(task.id)
    print("✓ Cleanup done.\n")

if __name__ == "__main__":
    main()
