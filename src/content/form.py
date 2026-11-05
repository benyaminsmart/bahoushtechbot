"""Start Project form content for Bahoush Tech bot (extracted from start-project.html)."""

PROJECT_FORM = {
    "title": "Start Your Project",
    "intro": (
        "Great! Let's turn your idea into reality. "
        "I'll ask you a few quick questions — it takes about 2 minutes."
    ),
    "steps": [
        {
            "id": "name",
            "question": "👤 What's your full name?",
            "type": "text",
        },
        {
            "id": "email",
            "question": "📧 What's your email address?",
            "type": "text",
        },
        {
            "id": "service_type",
            "question": "🎯 What type of service do you need?",
            "type": "choice",
            "options": [
                "AI & Machine Learning",
                "Web2 (Websites & Platforms)",
                "Web3 & Blockchain",
                "Automation & Bots",
                "Other",
            ],
        },
        {
            "id": "product_type",
            "question": "📦 What type of product?",
            "type": "choice",
            "options": ["Website", "Mobile App", "Platform / SaaS"],
        },
        {
            "id": "delivery",
            "question": "🚀 What do you need?",
            "type": "choice",
            "options": [
                "Code Only (You run it)",
                "Code + Deployment (We run it)",
            ],
        },
        {
            "id": "budget",
            "question": "💰 Estimated budget?",
            "type": "choice",
            "options": [
                "Under AED 5,000",
                "AED 5,000 - AED 20,000",
                "AED 20,000 - AED 50,000",
                "AED 50,000+",
                "Not sure yet",
            ],
        },
        {
            "id": "details",
            "question": "📝 Any additional details about your project? (or type /skip)",
            "type": "text",
            "optional": True,
        },
    ],
    "success": (
        "✅ Thank you! Your project request has been received.\n\n"
        "Our team will review it and get back to you soon at the email you provided.\n\n"
        "🚀 Let's turn your idea into reality!"
    ),
}
