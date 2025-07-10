import json
from datetime import datetime, timedelta
from enum import Enum

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TodoList:
    def __init__(self, filename="todos.json"):
        self.filename = filename
        self.todos = self.load_todos()
        self.next_id = self.get_next_id()
    
    def load_todos(self):
        """Load todos from file."""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_todos(self):
        """Save todos to file."""
        with open(self.filename, 'w') as f:
            json.dump(self.todos, f, indent=2)
    
    def get_next_id(self):
        """Get the next available ID."""
        if not self.todos:
            return 1
        return max(todo['id'] for todo in self.todos) + 1
    
    def add_todo(self, title, description="", priority=Priority.MEDIUM, due_date=None):
        """Add a new todo item."""
        todo = {
            'id': self.next_id,
            'title': title,
            'description': description,
            'priority': priority.value,
            'due_date': due_date,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'completed_at': None
        }
        
        self.todos.append(todo)
        self.next_id += 1
        self.save_todos()
        return todo['id']
    
    def complete_todo(self, todo_id):
        """Mark a todo as completed."""
        for todo in self.todos:
            if todo['id'] == todo_id:
                todo['completed'] = True
                todo['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_todos()
                return True
        return False
    
    def delete_todo(self, todo_id):
        """Delete a todo item."""
        self.todos = [todo for todo in self.todos if todo['id'] != todo_id]
        self.save_todos()
    
    def update_todo(self, todo_id, title=None, description=None, priority=None, due_date=None):
        """Update a todo item."""
        for todo in self.todos:
            if todo['id'] == todo_id:
                if title is not None:
                    todo['title'] = title
                if description is not None:
                    todo['description'] = description
                if priority is not None:
                    todo['priority'] = priority.value
                if due_date is not None:
                    todo['due_date'] = due_date
                self.save_todos()
                return True
        return False
    
    def get_priority_symbol(self, priority):
        """Get symbol for priority level."""
        symbols = {1: "🟢", 2: "🟡", 3: "🔴"}
        return symbols.get(priority, "⚪")
    
    def get_priority_name(self, priority):
        """Get name for priority level."""
        names = {1: "Low", 2: "Medium", 3: "High"}
        return names.get(priority, "Unknown")
    
    def is_overdue(self, due_date):
        """Check if a task is overdue."""
        if not due_date:
            return False
        try:
            due = datetime.strptime(due_date, '%Y-%m-%d')
            return due.date() < datetime.now().date()
        except:
            return False
    
    def display_todos(self, show_completed=False, filter_priority=None):
        """Display todos with formatting."""
        filtered_todos = []
        
        for todo in self.todos:
            if not show_completed and todo['completed']:
                continue
            if filter_priority and todo['priority'] != filter_priority.value:
                continue
            filtered_todos.append(todo)
        
        if not filtered_todos:
            print("No todos found.")
            return
        
        filtered_todos.sort(key=lambda x: (
            -x['priority'], 
            x['due_date'] or '9999-12-31'  
        ))
        
        print("\n=== Your To-Do List ===")
        for todo in filtered_todos:
            status = "✅" if todo['completed'] else "⬜"
            priority_symbol = self.get_priority_symbol(todo['priority'])
            
            print(f"\n{status} [{todo['id']}] {priority_symbol} {todo['title']}")
            
            if todo['description']:
                print(f"   📝 {todo['description']}")
            
            if todo['due_date']:
                due_date = todo['due_date']
                if self.is_overdue(due_date) and not todo['completed']:
                    print(f"   ⏰ Due: {due_date} (OVERDUE)")
                else:
                    print(f"   📅 Due: {due_date}")
            
            print(f"   🏷️  Priority: {self.get_priority_name(todo['priority'])}")
            
            if todo['completed']:
                print(f"   ✅ Completed: {todo['completed_at']}")
    
    def get_stats(self):
        """Get todo statistics."""
        total = len(self.todos)
        completed = len([t for t in self.todos if t['completed']])
        pending = total - completed
        overdue = len([t for t in self.todos if self.is_overdue(t['due_date']) and not t['completed']])
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'overdue': overdue,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }


def main():
    todo_list = TodoList()
    
    print("📝 Smart To-Do List")
    print("===================")
    
    while True:
        print("\n📋 Options:")
        print("1. Add todo")
        print("2. View todos")
        print("3. Complete todo")
        print("4. Update todo")
        print("5. Delete todo")
        print("6. View statistics")
        print("7. View completed todos")
        print("8. Exit")
        
        choice = input("\nChoose an option (1-8): ").strip()
        
        if choice == "1":
            title = input("Enter todo title: ").strip()
            description = input("Enter description (optional): ").strip()
            
            print("Priority levels: 1=Low, 2=Medium, 3=High")
            try:
                priority_num = int(input("Enter priority (1-3, default 2): ") or "2")
                priority = Priority(priority_num)
            except ValueError:
                priority = Priority.MEDIUM
            
            due_date = input("Enter due date (YYYY-MM-DD, optional): ").strip()
            if not due_date:
                due_date = None
            
            todo_id = todo_list.add_todo(title, description, priority, due_date)
            print(f"✅ Todo added with ID: {todo_id}")
        
        elif choice == "2":
            print("Filter options:")
            print("1. All pending todos")
            print("2. High priority only")
            print("3. Medium priority only")
            print("4. Low priority only")
            
            filter_choice = input("Choose filter (1-4, default 1): ").strip() or "1"
            
            filter_priority = None
            if filter_choice == "2":
                filter_priority = Priority.HIGH
            elif filter_choice == "3":
                filter_priority = Priority.MEDIUM
            elif filter_choice == "4":
                filter_priority = Priority.LOW
            
            todo_list.display_todos(filter_priority=filter_priority)
        
        elif choice == "3":
            try:
                todo_id = int(input("Enter todo ID to complete: "))
                if todo_list.complete_todo(todo_id):
                    print("✅ Todo marked as completed!")
                else:
                    print("❌ Todo not found.")
            except ValueError:
                print("❌ Invalid ID.")
        
        elif choice == "4":
            try:
                todo_id = int(input("Enter todo ID to update: "))
                title = input("New title (press Enter to keep current): ").strip()
                description = input("New description (press Enter to keep current): ").strip()
                due_date = input("New due date (YYYY-MM-DD, press Enter to keep current): ").strip()
                
                if todo_list.update_todo(
                    todo_id, 
                    title if title else None,
                    description if description else None,
                    due_date=due_date if due_date else None
                ):
                    print("✅ Todo updated!")
                else:
                    print("❌ Todo not found.")
            except ValueError:
                print("❌ Invalid ID.")
        
        elif choice == "5":
            try:
                todo_id = int(input("Enter todo ID to delete: "))
                confirm = input("Are you sure? (y/n): ").lower()
                if confirm == 'y':
                    todo_list.delete_todo(todo_id)
                    print("✅ Todo deleted!")
                else:
                    print("❌ Deletion cancelled.")
            except ValueError:
                print("❌ Invalid ID.")
        
        elif choice == "6":
            stats = todo_list.get_stats()
            print(f"\n📊 Statistics:")
            print(f"Total todos: {stats['total']}")
            print(f"Completed: {stats['completed']}")
            print(f"Pending: {stats['pending']}")
            print(f"Overdue: {stats['overdue']}")
            print(f"Completion rate: {stats['completion_rate']:.1f}%")
        
        elif choice == "7":
            todo_list.display_todos(show_completed=True)
        
        elif choice == "8":
            print("👋 Stay productive!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
