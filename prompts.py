"""Prompt templates and configuration for content generation"""

import re
from typing import Dict, List

# Content types configuration
CONTENT_TYPES = {
    "Blog Post": {
        "description": "Long-form blog article",
        "default_length": "Long",
        "default_tone": "Professional",
    },
    "Product Description": {
        "description": "Product or service description",
        "default_length": "Medium",
        "default_tone": "Persuasive",
    },
    "Marketing Email": {
        "description": "Promotional email",
        "default_length": "Medium",
        "default_tone": "Persuasive",
    },
    "Cold Email": {
        "description": "Cold outreach email",
        "default_length": "Short",
        "default_tone": "Professional",
    },
    "Instagram Caption": {
        "description": "Social media caption",
        "default_length": "Short",
        "default_tone": "Casual",
    },
    "LinkedIn Post": {
        "description": "Professional social post",
        "default_length": "Medium",
        "default_tone": "Professional",
    },
    "Facebook Ad": {
        "description": "Facebook advertisement",
        "default_length": "Short",
        "default_tone": "Persuasive",
    },
    "Google Ad Copy": {
        "description": "Google Ads text",
        "default_length": "Short",
        "default_tone": "Persuasive",
    },
    "SEO Description": {
        "description": "Meta description for SEO",
        "default_length": "Short",
        "default_tone": "Professional",
    },
    "YouTube Script": {
        "description": "Video script for YouTube",
        "default_length": "Long",
        "default_tone": "Friendly",
    },
}

# Tones
TONES = [
    "Professional",
    "Friendly",
    "Persuasive",
    "Luxury",
    "Casual",
    "Funny",
    "Technical",
    "Inspirational",
    "Urgent",
    "Educational",
]

# Styles
STYLES = [
    "Concise",
    "Detailed",
    "Storytelling",
    "Corporate",
    "Emotional",
    "Data-driven",
    "Question-based",
    "Bullet-points",
    "Narrative",
    "Comparative",
]

# Lengths
LENGTHS = {
    "Short": "100-200 words",
    "Medium": "300-500 words",
    "Long": "800-1500 words",
}

# Languages
LANGUAGES = {
    "English": "English",
    "Hindi": "Hindi",
    "Marathi": "Marathi",
}


class PromptBuilder:
    """Build dynamic prompts for content generation"""

    @staticmethod
    def build_prompt(
        content_type: str,
        topic: str,
        audience: str,
        tone: str,
        style: str,
        length: str,
        language: str,
        keywords: str,
        creativity: float = 0.7,
    ) -> str:
        """Build a comprehensive prompt for content generation"""

        # Word count range based on length
        length_range = LENGTHS.get(length, "300-500")

        # Base prompt structure
        prompt = f"""Write a {content_type.lower()} about "{topic}".

Target Audience: {audience}
Tone: {tone}
Style: {style}
Length: {length_range}
Language: {language}

Instructions:
1. Make it engaging, human-like, and authentic.
2. Use natural language flow.
3. Incorporate the following keywords naturally: {keywords if keywords else "N/A"}
4. Ensure the content is relevant and valuable to the audience.
5. Follow the specified tone and style throughout.
6. Make it unique and non-generic.
7. Proper formatting with paragraphs, not one long block of text.
8. No markdown, just plain text formatted nicely.

Important: Generate ONLY the content, no headers, no "Here is...", no explanations. Start directly with the content."""

        return prompt

    @staticmethod
    def build_rewrite_prompt(
        original_text: str,
        rewrite_type: str,
        tone: str = None,
        style: str = None,
    ) -> str:
        """Build prompt for rewriting existing content"""

        if rewrite_type == "shorter":
            return f"""Make this text shorter and more concise while keeping the key message intact. Remove unnecessary words and statements. Keep it punchy and direct.

Original text:
{original_text}

Important: Return ONLY the rewritten text, no explanations."""

        elif rewrite_type == "longer":
            return f"""Expand this text with more details, examples, and explanations. Make it more comprehensive while maintaining the core message.

Original text:
{original_text}

Important: Return ONLY the expanded text, no explanations."""

        elif rewrite_type == "grammar":
            return f"""Improve the grammar, spelling, and punctuation of this text. Make it more professional and polished. Keep the exact same meaning and tone.

Original text:
{original_text}

Important: Return ONLY the improved text, no explanations."""

        elif rewrite_type == "seo":
            return f"""Optimize this text for SEO while maintaining readability and meaning. Improve keyword placement, add relevant keywords naturally, and structure it better for search engines.

Original text:
{original_text}

Important: Return ONLY the optimized text, no explanations."""

        return original_text

    @staticmethod
    def build_enhancement_prompt(
        original_text: str,
        enhancement_type: str,
    ) -> str:
        """Build prompt for enhancing content"""

        if enhancement_type == "add_cta":
            return f"""Add a compelling call-to-action to the end of this text. Make it action-oriented and relevant.

Original text:
{original_text}

Important: Return ONLY the text with CTA added at the end, no explanations."""

        elif enhancement_type == "add_examples":
            return f"""Add relevant examples and real-world scenarios to this text to make it more concrete and relatable.

Original text:
{original_text}

Important: Return ONLY the enhanced text, no explanations."""

        elif enhancement_type == "make_compelling":
            return f"""Rewrite this to be more compelling, engaging, and persuasive. Add emotional appeal and make the reader want to take action.

Original text:
{original_text}

Important: Return ONLY the enhanced text, no explanations."""

        return original_text


class ContentAnalyzer:
    """Analyze generated content"""

    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text"""
        return len(text.split())

    @staticmethod
    def count_characters(text: str) -> int:
        """Count characters in text"""
        return len(text)

    @staticmethod
    def estimate_reading_time(text: str) -> int:
        """Estimate reading time in minutes (avg 200 words/min)"""
        words = ContentAnalyzer.count_words(text)
        minutes = max(1, words // 200)
        return minutes

    @staticmethod
    def calculate_keyword_density(text: str, keywords: str) -> Dict[str, float]:
        """Calculate keyword density in text"""
        if not keywords:
            return {}

        keyword_list = [kw.strip().lower() for kw in keywords.split(",")]
        text_lower = text.lower()
        word_count = ContentAnalyzer.count_words(text)

        density = {}
        for keyword in keyword_list:
            # Count occurrences
            count = len(re.findall(r"\b" + re.escape(keyword) + r"\b", text_lower))
            if count > 0:
                percentage = (count / word_count) * 100
                density[keyword] = round(percentage, 2)

        return density

    @staticmethod
    def estimate_seo_score(text: str, keywords: str) -> int:
        """Estimate SEO score (0-100)"""
        score = 50

        # Length check
        words = ContentAnalyzer.count_words(text)
        if words > 300:
            score += 10
        if words > 800:
            score += 10

        # Keyword density
        if keywords:
            density = ContentAnalyzer.calculate_keyword_density(text, keywords)
            if len(density) > 0:
                score += 15
                # Penalize overstuffing
                for pct in density.values():
                    if pct > 3:
                        score -= 5

        # Readability (simple check for paragraphs)
        paragraphs = text.split("\n\n")
        if len(paragraphs) > 2:
            score += 10

        return min(100, max(0, score))

    @staticmethod
    def calculate_readability_score(text: str) -> int:
        """Calculate readability score (Flesch-Kincaid simplified)"""
        words = len(text.split())
        sentences = len(re.split(r"[.!?]+", text))
        syllables = sum(
            text.lower().count(vowel)
            for vowel in ["a", "e", "i", "o", "u"]
        )

        if words == 0 or sentences == 0:
            return 50

        # Simplified readability calculation
        score = 206.835 - 1.015 * (words / max(1, sentences)) - 84.6 * (
            syllables / max(1, words)
        )
        score = max(0, min(100, score))

        return int(score)

    @staticmethod
    def detect_tone_indicators(text: str) -> List[str]:
        """Detect tone indicators in text"""
        tones = []

        text_lower = text.lower()

        # Professional indicators
        if any(word in text_lower for word in ["therefore", "furthermore", "however"]):
            tones.append("Professional")

        # Casual indicators
        if any(
            word in text_lower
            for word in ["hey", "cool", "awesome", "yeah", "gonna", "wanna"]
        ):
            tones.append("Casual")

        # Persuasive indicators
        if any(
            word in text_lower
            for word in ["should", "must", "don't miss", "limited", "exclusive"]
        ):
            tones.append("Persuasive")

        # Question indicators
        if text.count("?") > text.count(".") / 2:
            tones.append("Question-based")

        return tones if tones else ["Neutral"]
