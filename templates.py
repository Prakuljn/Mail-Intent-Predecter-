# Base templates
TEMPLATES = {
    "User Manual": """Hello,

Thank you for reaching out. Please find our user manual here:
👉 https://example.com/manual

Best regards,
Support Team
""",

    "Product Info": """Hello,

Thanks for your interest! You can read more about our product here:
👉 https://example.com/info

Best regards,
Support Team
""",

    "Installation": """Hello,

We’re glad to help. Please follow our installation guide here:
👉 https://example.com/install

Best regards,
Support Team
"""
}

# Combination templates
COMBINATIONS = {
    frozenset(["User Manual", "Product Info"]): """Hello,

We understand you’d like the user manual and product information.

👉 User Manual: https://example.com/manual
👉 Product Info: https://example.com/info

Best regards,
Support Team
""",
    frozenset(["Product Info", "Installation"]): """Hello,

We understand you’d like the product information and installation guide.

👉 Product Info: https://example.com/info
👉 Installation Guide: https://example.com/install

Best regards,
Support Team
""",

    frozenset(["User Manual", "Installation"]): """Hello,

We understand you’d like the user manual and installation guide.

👉 User Manual: https://example.com/manual
👉 Installation Guide: https://example.com/install
Best regards,
Support Team
""",

    frozenset(["User Manual", "Installation"]): """Hello,

We understand you’d like the user manual and installation guide.

👉 User Manual: https://example.com/manual
👉 Installation Guide: https://example.com/install

Best regards,
Support Team
""",

    

    frozenset(["User Manual", "Product Info", "Installation"]): """Hello,

We understand you’d like the user manual, product information, and installation guide.

👉 User Manual: https://example.com/manual
👉 Product Info: https://example.com/info
👉 Installation Guide: https://example.com/install

Best regards,
Support Team
"""
}
