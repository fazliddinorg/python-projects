import hashlib
import json
import random
import string
from urllib.parse import urlparse

class URLShortener:
    def __init__(self, storage_file="urls.json"):
        self.storage_file = storage_file
        self.urls = self.load_urls()
        self.base_url = "https://short.ly/"
    
    def load_urls(self):
        """Load URLs from storage file."""
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_urls(self):
        """Save URLs to storage file."""
        with open(self.storage_file, 'w') as f:
            json.dump(self.urls, f, indent=2)
    
    def validate_url(self, url):
        """Validate if URL is properly formatted."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def generate_short_code(self, length=6):
        """Generate a random short code."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def generate_hash_code(self, url):
        """Generate a hash-based short code."""
        return hashlib.md5(url.encode()).hexdigest()[:8]
    
    def shorten_url(self, long_url, custom_code=None, use_hash=False):
        """Shorten a URL with optional custom code."""
        if not self.validate_url(long_url):
            return None, "Invalid URL format"
        
        # Check if URL is already shortened
        for code, data in self.urls.items():
            if data['long_url'] == long_url:
                return f"{self.base_url}{code}", "URL already exists"
        
        # Generate short code
        if custom_code:
            if custom_code in self.urls:
                return None, "Custom code already exists"
            short_code = custom_code
        elif use_hash:
            short_code = self.generate_hash_code(long_url)
            if short_code in self.urls:
                short_code = self.generate_short_code()
        else:
            short_code = self.generate_short_code()
            while short_code in self.urls:
                short_code = self.generate_short_code()
        
        # Store URL
        self.urls[short_code] = {
            'long_url': long_url,
            'clicks': 0,
            'created_at': str(hash(long_url))  # Simple timestamp substitute
        }
        
        self.save_urls()
        return f"{self.base_url}{short_code}", "Success"
    
    def expand_url(self, short_url):
        """Expand a shortened URL."""
        # Extract code from URL
        if short_url.startswith(self.base_url):
            code = short_url[len(self.base_url):]
        else:
            code = short_url
        
        if code in self.urls:
            # Increment click count
            self.urls[code]['clicks'] += 1
            self.save_urls()
            return self.urls[code]['long_url']
        
        return None
    
    def get_stats(self, short_url):
        """Get statistics for a shortened URL."""
        if short_url.startswith(self.base_url):
            code = short_url[len(self.base_url):]
        else:
            code = short_url
        
        if code in self.urls:
            return self.urls[code]
        return None
    
    def list_urls(self):
        """List all shortened URLs."""
        if not self.urls:
            print("No URLs shortened yet.")
            return
        
        print("\n=== Your Shortened URLs ===")
        for code, data in self.urls.items():
            short_url = f"{self.base_url}{code}"
            print(f"Short: {short_url}")
            print(f"Long:  {data['long_url']}")
            print(f"Clicks: {data['clicks']}")
            print("-" * 50)

def main():
    shortener = URLShortener()
    
    print("🔗 URL Shortener")
    print("================")
    
    while True:
        print("\n📋 Options:")
        print("1. Shorten URL")
        print("2. Expand URL")
        print("3. Get URL stats")
        print("4. List all URLs")
        print("5. Exit")
        
        choice = input("\nChoose an option (1-5): ").strip()
        
        if choice == "1":
            long_url = input("Enter URL to shorten: ").strip()
            custom_code = input("Enter custom code (optional): ").strip() or None
            use_hash = input("Use hash-based code? (y/n): ").lower() == 'y'
            
            short_url, message = shortener.shorten_url(long_url, custom_code, use_hash)
            
            if short_url:
                print(f"✅ {message}")
                print(f"Short URL: {short_url}")
            else:
                print(f"❌ Error: {message}")
        
        elif choice == "2":
            short_url = input("Enter short URL to expand: ").strip()
            long_url = shortener.expand_url(short_url)
            
            if long_url:
                print(f"✅ Original URL: {long_url}")
            else:
                print("❌ Short URL not found")
        
        elif choice == "3":
            short_url = input("Enter short URL for stats: ").strip()
            stats = shortener.get_stats(short_url)
            
            if stats:
                print(f"\n📊 Statistics:")
                print(f"Original URL: {stats['long_url']}")
                print(f"Total clicks: {stats['clicks']}")
            else:
                print("❌ Short URL not found")
        
        elif choice == "4":
            shortener.list_urls()
        
        elif choice == "5":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
