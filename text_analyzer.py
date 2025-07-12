import re
from collections import Counter
import string

class TextAnalyzer:
    def __init__(self):
        self.text = ""
        self.sentences = []
        self.words = []
        self.paragraphs = []
    
    def load_text(self, text):
        """Load text for analysis."""
        self.text = text
        self.sentences = self.split_sentences(text)
        self.words = self.extract_words(text)
        self.paragraphs = self.split_paragraphs(text)
    
    def split_sentences(self, text):
        """Split text into sentences."""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def extract_words(self, text):
        """Extract words from text."""
        # Remove punctuation and convert to lowercase
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text.split()
    
    def split_paragraphs(self, text):
        """Split text into paragraphs."""
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]
    
    def basic_stats(self):
        """Get basic text statistics."""
        return {
            'characters': len(self.text),
            'characters_no_spaces': len(self.text.replace(' ', '')),
            'words': len(self.words),
            'sentences': len(self.sentences),
            'paragraphs': len(self.paragraphs),
            'avg_words_per_sentence': len(self.words) / len(self.sentences) if self.sentences else 0,
            'avg_sentences_per_paragraph': len(self.sentences) / len(self.paragraphs) if self.paragraphs else 0
        }
    
    def word_frequency(self, top_n=10):
        """Get word frequency analysis."""
        if not self.words:
            return {}
        
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        filtered_words = [word for word in self.words if word not in stop_words and len(word) > 2]
        
        counter = Counter(filtered_words)
        return counter.most_common(top_n)
    
    def readability_score(self):
        """Calculate Flesch Reading Ease score."""
        if not self.sentences or not self.words:
            return 0
        
        total_words = len(self.words)
        total_sentences = len(self.sentences)
        total_syllables = sum(self.count_syllables(word) for word in self.words)
        
        if total_sentences == 0 or total_words == 0:
            return 0
        
        # Flesch Reading Ease formula
        score = 206.835 - (1.015 * (total_words / total_sentences)) - (84.6 * (total_syllables / total_words))
        return max(0, min(100, score))
    
    def count_syllables(self, word):
        """Count syllables in a word (approximation)."""
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        
        if word[0] in vowels:
            count += 1
        
        for i in range(1, len(word)):
            if word[i] in vowels and word[i-1] not in vowels:
                count += 1
        
        if word.endswith('e'):
            count -= 1
        
        if count == 0:
            count = 1
        
        return count
    
    def readability_level(self, score):
        """Get readability level description."""
        if score >= 90:
            return "Very Easy (5th grade level)"
        elif score >= 80:
            return "Easy (6th grade level)"
        elif score >= 70:
            return "Fairly Easy (7th grade level)"
        elif score >= 60:
            return "Standard (8th-9th grade level)"
        elif score >= 50:
            return "Fairly Difficult (10th-12th grade level)"
        elif score >= 30:
            return "Difficult (College level)"
        else:
            return "Very Difficult (Graduate level)"
    
    def sentiment_analysis(self):
        """Basic sentiment analysis."""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome', 'brilliant', 'perfect', 'love', 'like', 'happy', 'joy', 'pleased', 'satisfied', 'delighted', 'thrilled', 'excited', 'optimistic', 'positive', 'beautiful', 'successful', 'win', 'winner', 'best', 'better', 'improve', 'success', 'achievement', 'accomplish']
        
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'angry', 'sad', 'disappointed', 'frustrated', 'annoyed', 'upset', 'worried', 'concerned', 'problem', 'issue', 'fail', 'failure', 'worst', 'worse', 'negative', 'difficult', 'hard', 'challenging', 'struggle', 'trouble', 'wrong', 'error', 'mistake', 'damage']
        
        positive_count = sum(1 for word in self.words if word in positive_words)
        negative_count = sum(1 for word in self.words if word in negative_words)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return "Neutral", 0
        
        sentiment_score = (positive_count - negative_count) / total_sentiment_words
        
        if sentiment_score > 0.1:
            return "Positive", sentiment_score
        elif sentiment_score < -0.1:
            return "Negative", sentiment_score
        else:
            return "Neutral", sentiment_score
    
    def generate_report(self):
        """Generate a comprehensive text analysis report."""
        stats = self.basic_stats()
        word_freq = self.word_frequency()
        readability = self.readability_score()
        sentiment, sentiment_score = self.sentiment_analysis()
        
        report = f"""
=== TEXT ANALYSIS REPORT ===

📊 BASIC STATISTICS:
Characters: {stats['characters']:,}
Characters (no spaces): {stats['characters_no_spaces']:,}
Words: {stats['words']:,}
Sentences: {stats['sentences']:,}
Paragraphs: {stats['paragraphs']:,}
Average words per sentence: {stats['avg_words_per_sentence']:.1f}
Average sentences per paragraph: {stats['avg_sentences_per_paragraph']:.1f}

📚 READABILITY:
Flesch Reading Ease Score: {readability:.1f}
Reading Level: {self.readability_level(readability)}

💭 SENTIMENT ANALYSIS:
Overall Sentiment: {sentiment}
Sentiment Score: {sentiment_score:.2f}

🔤 MOST FREQUENT WORDS:"""
        
        for word, count in word_freq:
            report += f"\n'{word}': {count} times"
        
        return report

def main():
    analyzer = TextAnalyzer()
    
    print("📝 Text Analyzer")
    print("================")
    
    while True:
        print("\n📋 Options:")
        print("1. Analyze text input")
        print("2. Analyze text from file")
        print("3. Exit")
        
        choice = input("\nChoose an option (1-3): ").strip()
        
        if choice == "1":
            print("\nEnter your text (press Enter twice to finish):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            
            text = "\n".join(lines)
            if text.strip():
                analyzer.load_text(text)
                print(analyzer.generate_report())
            else:
                print("❌ No text entered.")
        
        elif choice == "2":
            filename = input("Enter filename: ").strip()
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    text = file.read()
                    analyzer.load_text(text)
                    print(analyzer.generate_report())
            except FileNotFoundError:
                print(f"❌ File '{filename}' not found.")
            except Exception as e:
                print(f"❌ Error reading file: {e}")
        
        elif choice == "3":
            print("👋 Happy analyzing!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
