"""
Automatically detect the category of an electronic product
from its title.

This module is brand-independent and works with
any electronic brand available on Amazon.
"""

import re


CATEGORY_PATTERNS = {

    "Smartphone": [

        r"\bsmartphone\b",
        r"\bphone\b",
        r"\bmobile\b",

    ],

    "Laptop": [

        r"\blaptop\b",
        r"\bnotebook\b",
        r"\bultrabook\b",

    ],

    "Tablet": [

        r"\btablet\b",
        r"\btab\b",
        r"\bpad\b",

    ],

    "Smartwatch": [

        r"\bsmartwatch\b",
        r"\bwatch\b",

    ],

    "Earbuds": [

        r"\bearbuds\b",
        r"\bheadphones\b",
        r"\bheadset\b",
        r"\bearphone\b",
        r"\bearphones\b",
        r"\btws\b",

        # Sony naming convention
        r"\bwh-[a-z0-9-]+\b",
        r"\bwf-[a-z0-9-]+\b",

    ],

    "Monitor": [

        r"\bmonitor\b",
        r"\bdisplay\b",

    ],

    "Television": [

        r"\btv\b",
        r"\btelevision\b",
        r"\boled\b",
        r"\bqled\b",
        r"\bmini led\b",

    ],

    "Camera": [

        r"\bcamera\b",
        r"\bmirrorless\b",
        r"\bdslr\b",
        r"\baction camera\b",
        r"\bcamcorder\b",

    ],

    "Gaming Console": [

        r"\bconsole\b",
        r"\bhandheld\b",
        r"\bgaming console\b",

    ],

    "Speaker": [

        r"\bspeaker\b",
        r"\bsoundbar\b",

    ],

    "Printer": [

        r"\bprinter\b",
        r"\bmultifunction printer\b",

    ],

    "Router": [

        r"\brouter\b",
        r"\bwi[- ]?fi\b",
        r"\bmesh\b",

    ],

}


CATEGORY_PRIORITY = [

    "Gaming Console",
    "Camera",
    "Laptop",
    "Tablet",
    "Smartwatch",
    "Earbuds",
    "Monitor",
    "Television",
    "Speaker",
    "Printer",
    "Router",
    "Smartphone",

]


def detect_category(
    product_name: str,
) -> str:
    """
    Detect the electronic product category.

    Returns
    -------
    str
        Category name or "Unknown".
    """

    if not product_name:

        return "Unknown"

    text = product_name.lower().strip()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    for category in CATEGORY_PRIORITY:

        patterns = CATEGORY_PATTERNS[category]

        for pattern in patterns:

            if re.search(pattern, text):

                return category

    return "Unknown"