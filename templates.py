"""Template management and prebuilt templates"""

from typing import List, Dict, Any


class TemplateLibrary:
    """Manage prebuilt content templates"""

    # Prebuilt templates - these are seeded into the database on first run
    PREBUILT_TEMPLATES = {
        "Product Launch Email": {
            "content_type": "Marketing Email",
            "description": "Email template for announcing a new product launch",
            "template_text": """Subject: Introducing {product_name} - Revolutionary Solution for {problem}

Dear {audience},

We're thrilled to announce the launch of {product_name}, a breakthrough solution designed specifically for {target_segment}.

For years, {target_audience} have struggled with {problem}. Today, that changes.

{product_name} delivers:
• {benefit_1}
• {benefit_2}
• {benefit_3}

What makes it different:
{unique_selling_point}

Early adopters will receive {special_offer}.

Ready to transform how you {action}?

[CALL_TO_ACTION_BUTTON]

Best regards,
{company_name}
{contact_info}""",
        },
        "Startup LinkedIn Post": {
            "content_type": "LinkedIn Post",
            "description": "LinkedIn post template for startup announcements",
            "template_text": """Excited to announce that {startup_name} is officially live! 🚀

After months of {development_journey}, we've built something we truly believe will change {industry_area}.

The problem: {problem_statement}

Our solution: {solution_overview}

We're already helping {customer_type} to {customer_outcome}.

Special thanks to {acknowledgments}.

If you're interested in {value_proposition}, I'd love to chat. Feel free to reach out!

{call_to_action_link}

#Startup #Innovation #Entrepreneur #{industry_hashtag}""",
        },
        "Ecommerce Product Copy": {
            "content_type": "Product Description",
            "description": "Product description for ecommerce platforms",
            "template_text": """**{product_name}**

**Price:** {price}

**Overview:**
{product_overview}

**Key Features:**
• {feature_1}
• {feature_2}
• {feature_3}
• {feature_4}

**Benefits:**
✓ {benefit_1}
✓ {benefit_2}
✓ {benefit_3}

**Specifications:**
- Material: {material}
- Size: {size}
- Weight: {weight}
- Color Options: {colors}

**Why Choose This?**
{competitive_advantage}

**Customer Testimonial:**
"{testimonial}"
— {customer_name}, {customer_title}

**Limited Time Offer:**
{offer_details}

[ADD_TO_CART]
[BUY_NOW]""",
        },
        "Festival Sale Ad": {
            "content_type": "Facebook Ad",
            "description": "Festival season promotional ad copy",
            "template_text": """{festival_name} Sale is LIVE! 🎉

Get {discount}% OFF on {product_category}!

✨ Limited time only - {sale_duration}
✨ Free shipping on orders above {threshold}
✨ Exclusive {festival_name} bundles

Shop now and get:
→ {offer_1}
→ {offer_2}
→ {offer_3}

Don't miss out! Sale ends {end_date}

SHOP NOW → {deal_link}

#FestivalSale #{festival_name_hashtag} #DealsOfTheDay""",
        },
        "Cold Outreach Email": {
            "content_type": "Cold Email",
            "description": "Template for cold outreach emails",
            "template_text": """Subject: Quick question about {company_name}

Hi {prospect_name},

I came across your work at {company_name} and noticed you're leading {project/initiative}.

I help {target_audience} achieve {desired_outcome} through {solution_brief}.

Given your focus on {their_focus_area}, I thought you might find value in {specific_value}.

Three quick reasons why companies like {similar_company_1}, {similar_company_2} work with us:
1. {reason_1}
2. {reason_2}
3. {reason_3}

Would you be open to a brief 15-minute call next week to explore if there's a fit?

No pressure at all if the timing isn't right.

{your_name}
{your_title}
{your_company}
{contact_info}""",
        },
        "SEO Blog Intro": {
            "content_type": "Blog Post",
            "description": "Blog introduction optimized for SEO",
            "template_text": """# {primary_keyword}: Complete Guide for {target_audience}

## Quick Answer:
{quick_answer_to_query}

---

Looking to learn about {topic}? You're in the right place.

In this comprehensive guide, you'll discover:
- {section_1}
- {section_2}
- {section_3}
- {section_4}
- {section_5}

Whether you're a {audience_level} or {audience_level2}, this guide will walk you through everything you need to know.

Let's dive in.

---

## Table of Contents
1. {section_1}
2. {section_2}
3. {section_3}
4. {section_4}
5. {section_5}
6. {faq_section}

---

## {section_1}

{section_content}

---

**Key Takeaway:**
{key_learning}

---

*Last updated: [DATE]*
*Reading time: ~{reading_time} minutes*""",
        },
    }

    @staticmethod
    def get_prebuilt_templates() -> Dict[str, Dict[str, Any]]:
        """Get all prebuilt templates"""
        return TemplateLibrary.PREBUILT_TEMPLATES

    @staticmethod
    def get_template_by_name(name: str) -> Dict[str, Any]:
        """Get a specific template by name"""
        return TemplateLibrary.PREBUILT_TEMPLATES.get(name, {})

    @staticmethod
    def get_templates_by_type(content_type: str) -> Dict[str, Dict[str, Any]]:
        """Get templates by content type"""
        result = {}
        for name, template in TemplateLibrary.PREBUILT_TEMPLATES.items():
            if template.get("content_type") == content_type:
                result[name] = template
        return result

    @staticmethod
    def get_placeholders(template_name: str) -> List[str]:
        """Extract placeholders from template"""
        template = TemplateLibrary.get_template_by_name(template_name)
        template_text = template.get("template_text", "")

        import re

        placeholders = re.findall(r"\{(\w+)\}", template_text)
        return list(set(placeholders))  # Remove duplicates

    @staticmethod
    def render_template(template_name: str, values: Dict[str, str]) -> str:
        """Render template with provided values"""
        template = TemplateLibrary.get_template_by_name(template_name)
        template_text = template.get("template_text", "")

        rendered = template_text
        for placeholder, value in values.items():
            rendered = rendered.replace(f"{{{placeholder}}}", value or "")

        return rendered
