"""
Sample Indian Legal Documents for Testing
"""

SAMPLE_DOCUMENTS = [
    {
        "id": "income_tax_1",
        "title": "Income Tax Act - Section 2(1A)",
        "category": "Income Tax",
        "content": """Section 2(1A) - "Advance tax" means the tax payable under the provisions of Chapter XVII-C. 
        This section defines advance tax as the tax that is required to be paid in advance during the financial year, 
        as opposed to the tax paid after the completion of the financial year. The advance tax provisions are designed 
        to ensure regular flow of revenue to the government and to avoid the burden of paying the entire tax liability 
        at once at the end of the financial year.""",
        "entities": ["advance tax", "Chapter XVII-C", "financial year", "tax liability"]
    },
    {
        "id": "income_tax_2", 
        "title": "Income Tax Act - Section 10(1)",
        "category": "Income Tax",
        "content": """Section 10(1) - Agricultural income shall not be included in the total income. 
        Agricultural income means any rent or revenue derived from land which is situated in India and is used for 
        agricultural purposes, any income derived from such land by agriculture operations including processing of 
        agricultural produce raised or received as rent-in-kind, and any income derived from a farm house.""",
        "entities": ["agricultural income", "total income", "rent", "revenue", "agricultural purposes", "farm house"]
    },
    {
        "id": "gst_1",
        "title": "GST Act - Section 9(1)",
        "category": "GST",
        "content": """Section 9(1) - There shall be levied a tax called the central goods and services tax on all intra-State 
        supplies of goods or services or both, except on the supply of alcoholic liquor for human consumption, on the 
        taxable value of such supplies made by a taxable person in the course or furtherance of business.""",
        "entities": ["central goods and services tax", "intra-State supplies", "taxable value", "taxable person", "business"]
    },
    {
        "id": "gst_2",
        "title": "GST Act - Section 12(1)",
        "category": "GST", 
        "content": """Section 12(1) - The liability to pay tax on goods shall arise at the time of supply. 
        The time of supply of goods shall be the earliest of the following dates: the date of issue of invoice by the supplier, 
        the date of receipt of payment, or the date on which the goods are made available to the recipient.""",
        "entities": ["liability to pay tax", "time of supply", "invoice", "supplier", "payment", "recipient"]
    },
    {
        "id": "court_judgment_1",
        "title": "Supreme Court - Contract Law Judgment",
        "category": "Court Judgment",
        "content": """In the matter of breach of contract, the Supreme Court held that when a party fails to perform 
        their contractual obligations without lawful excuse, they are liable for damages. The court emphasized that 
        the measure of damages should be such as may fairly and reasonably be considered as arising naturally from 
        the breach of contract. The principle of mitigation of damages also applies, requiring the injured party to 
        take reasonable steps to minimize their losses.""",
        "entities": ["breach of contract", "contractual obligations", "damages", "mitigation of damages", "injured party"]
    },
    {
        "id": "court_judgment_2",
        "title": "High Court - Property Rights Judgment", 
        "category": "Court Judgment",
        "content": """The High Court ruled on property rights stating that ownership of immovable property requires clear 
        title and proper registration. The court noted that adverse possession can be claimed only after continuous 
        possession for a period of 12 years with the intention to possess as owner. The possession must be open, 
        continuous, and without the permission of the true owner.""",
        "entities": ["property rights", "immovable property", "clear title", "registration", "adverse possession", "continuous possession"]
    },
    {
        "id": "property_law_1",
        "title": "Transfer of Property Act - Section 54",
        "category": "Property Law",
        "content": """Section 54 - Sale defined: In a contract of sale of immovable property, the seller binds himself to 
        transfer the property in consideration of a price paid or promised or part-paid and part-promised. 
        Such contract, in the case of tangible immovable property of the value of one hundred rupees and upwards, 
        or in the case of a reversion or other intangible thing of the value of one hundred rupees and upwards, 
        can be made only by a registered instrument.""",
        "entities": ["contract of sale", "immovable property", "seller", "transfer", "consideration", "price", "registered instrument"]
    },
    {
        "id": "property_law_2",
        "title": "Registration Act - Section 17",
        "category": "Property Law", 
        "content": """Section 17 - Documents of which registration is compulsory: The following documents shall be registered, 
        namely: instruments of gift of immovable property, other non-testamentary instruments which purport or operate 
        to create, declare, assign, limit or extinguish any right, title or interest in immovable property of the value 
        of one hundred rupees and upwards. Registration ensures legal validity and provides public notice of the transaction.""",
        "entities": ["registration", "compulsory", "instruments of gift", "immovable property", "right", "title", "interest", "legal validity"]
    },
    {
        "id": "income_tax_3",
        "title": "Income Tax Act - Section 80C",
        "category": "Income Tax",
        "content": """Section 80C - Deduction in respect of life insurance premia, deferred annuity, provident fund, etc. 
        Any sum paid by an assessee, being the whole or any part of any premium paid to effect or keep in force an 
        insurance on the life of the assessee, his spouse or any child of the assessee, shall be allowed as deduction 
        subject to a maximum limit of Rs. 1,50,000 in a financial year.""",
        "entities": ["deduction", "life insurance", "premium", "assessee", "spouse", "child", "maximum limit", "financial year"]
    },
    {
        "id": "gst_3",
        "title": "GST Act - Section 22",
        "category": "GST",
        "content": """Section 22 - Compulsory registration: Every supplier shall be liable to be registered under this Act 
        in the State or Union territory from where he makes a taxable supply of goods or services or both if his 
        aggregate turnover in a financial year exceeds twenty lakh rupees. However, for special category states, 
        the threshold limit is ten lakh rupees.""",
        "entities": ["compulsory registration", "supplier", "taxable supply", "aggregate turnover", "financial year", "twenty lakh rupees", "special category states"]
    }
] 