import os
import shutil
from pathlib import Path

class FileOrganizer:
    def __init__(self, source_dir):
        self.source_dir = Path(source_dir)
        self.file_types = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'Spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
            'Presentations': ['.ppt', '.pptx', '.odp'],
            'Code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.c', '.h']
        }
    
    def create_folders(self):
        """Create folders for each file type."""
        for folder_name in self.file_types.keys():
            folder_path = self.source_dir / folder_name
            folder_path.mkdir(exist_ok=True)
            print(f"Created folder: {folder_name}")
    
    def get_file_category(self, file_path):
        """Determine which category a file belongs to."""
        file_extension = file_path.suffix.lower()
        
        for category, extensions in self.file_types.items():
            if file_extension in extensions:
                return category
        
        return "Others"
    
    def organize_files(self, create_others_folder=True):
        """Organize files into appropriate folders."""
        if not self.source_dir.exists():
            print(f"Source directory {self.source_dir} does not exist.")
            return
        
        # Create folders
        self.create_folders()
        
        # Create Others folder if needed
        if create_others_folder:
            others_folder = self.source_dir / "Others"
            others_folder.mkdir(exist_ok=True)
        
        moved_files = 0
        
        # Process each file
        for file_path in self.source_dir.iterdir():
            if file_path.is_file():
                category = self.get_file_category(file_path)
                
                if category == "Others" and not create_others_folder:
                    continue
                
                # Create destination path
                dest_folder = self.source_dir / category
                dest_path = dest_folder / file_path.name
                
                # Handle duplicate names
                counter = 1
                while dest_path.exists():
                    name_part = file_path.stem
                    extension = file_path.suffix
                    dest_path = dest_folder / f"{name_part}_{counter}{extension}"
                    counter += 1
                
                # Move file
                try:
                    shutil.move(str(file_path), str(dest_path))
                    print(f"Moved: {file_path.name} -> {category}/")
                    moved_files += 1
                except Exception as e:
                    print(f"Error moving {file_path.name}: {e}")
        
        print(f"\nOrganization complete! Moved {moved_files} files.")
    
    def preview_organization(self):
        """Preview what files will be moved where."""
        if not self.source_dir.exists():
            print(f"Source directory {self.source_dir} does not exist.")
            return
        
        categories = {}
        
        for file_path in self.source_dir.iterdir():
            if file_path.is_file():
                category = self.get_file_category(file_path)
                if category not in categories:
                    categories[category] = []
                categories[category].append(file_path.name)
        
        print("\n=== Organization Preview ===")
        for category, files in categories.items():
            print(f"\n{category} ({len(files)} files):")
            for file in files[:5]:  # Show first 5 files
                print(f"  - {file}")
            if len(files) > 5:
                print(f"  ... and {len(files) - 5} more files")

def main():
    print("=== File Organizer ===")
    
    # Get source directory
    source = input("Enter the path to organize (or press Enter for current directory): ").strip()
    if not source:
        source = "."
    
    organizer = FileOrganizer(source)
    
    # Preview organization
    organizer.preview_organization()
    
    # Ask for confirmation
    response = input("\nProceed with organization? (y/n): ").lower()
    if response == 'y':
        organizer.organize_files()
    else:
        print("Organization cancelled.")

if __name__ == "__main__":
    main()
