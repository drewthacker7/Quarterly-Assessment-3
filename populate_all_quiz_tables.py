import sqlite3

# Connect or create the database
conn = sqlite3.connect("quiz_bowl.db")
cursor = conn.cursor()

# Full question data for all tables
questions_data = {
    "python": [
        ("What is the output of print(type([1, 2, 3]))?", "<class 'tuple'>", "<class 'list'>", "<class 'set'>", "<class 'dict'>", "B"),
        ("Which keyword is used to create a function in Python?", "define", "func", "function", "def", "D"),
        ("What does len(\"Hello\") return?", "4", "5", "6", "Error", "B"),
        ("What is the correct file extension for Python files?", ".pt", ".py", ".python", ".p", "B"),
        ("What is the output of bool(0)?", "True", "False", "0", "None", "B"),
        ("How do you start a comment in Python?", "//", "<!--", "#", "#", "C"),
        ("What is the result of 3 ** 2?", "6", "9", "8", "5", "B"),
        ("Which collection is ordered and mutable?", "set", "tuple", "list", "dict", "C"),
        ("Which of the following is a Python data type?", "integer", "char", "str", "character", "C"),
        ("What is the result of int(\"10\") + 5?", "105", "15", "Error", "\"105\"", "B")
    ],
    "intermediate_accounting": [
        ("Which financial statement includes changes in equity?", "Balance Sheet", "Income Statement", "Statement of Cash Flows", "Statement of Stockholders' Equity", "D"),
        ("Treasury stock is reported as:", "An asset", "A liability", "A reduction of equity", "A revenue", "C"),
        ("Dividends in arrears apply to:", "Common stock", "Cumulative preferred stock", "Bonds", "Retained earnings", "B"),
        ("Stock dividends reduce:", "Common stock", "Retained earnings", "Treasury stock", "Paid-in capital", "B"),
        ("Par value is:", "Market price", "Issuance price", "Arbitrary legal capital", "Book value", "C"),
        ("Convertible bonds may be exchanged for:", "Cash", "Debt", "Equity", "Inventory", "C"),
        ("In a stock split, the number of shares:", "Decreases", "Remains unchanged", "Increases", "Is canceled", "C"),
        ("Which method is not used for treasury stock?", "FIFO", "Weighted average", "Cost method", "Par method", "A"),
        ("APIC stands for:", "Annual Payment In Capital", "Additional Paid-In Capital", "Asset Purchase In Cost", "Adjusted Price of Investments", "B"),
        ("A prior period adjustment affects:", "Current year net income", "Retained earnings beginning balance", "Assets", "Revenues", "B")
    ],
    "audit": [
        ("The audit opinion that indicates financial statements are fairly presented is:", "Adverse", "Disclaimer", "Qualified", "Unqualified", "D"),
        ("The responsibility for financial statements lies with:", "Auditors", "Shareholders", "Management", "SEC", "C"),
        ("What is an internal control?", "Tax compliance procedure", "Policy to ensure data reliability", "Audit test", "Trial balance", "B"),
        ("Substantive procedures:", "Control procedures", "Evaluate management", "Detect material misstatements", "Compile trial balances", "C"),
        ("Audit evidence must be:", "Expensive", "Persuasive", "Absolute", "Confirmed", "B"),
        ("What is a management representation letter?", "Legal document", "Internal memo", "Statement by auditors", "Confirmation by management", "D"),
        ("Analytical procedures compare:", "Notes to income", "Financial data over time", "Assets to invoices", "Debits to credits", "B"),
        ("Fraud risk is assessed during:", "Planning phase", "Review phase", "Final audit", "Test of controls", "A"),
        ("Materiality refers to:", "Total value", "Legal responsibility", "Significance to decision-making", "Disclosure level", "C"),
        ("A qualified opinion means:", "Everything is fine", "Severe errors", "Except for one issue, fairly presented", "No audit conducted", "C")
    ],
    "federal_taxation": [
        ("The standard deduction reduces:", "Tax liability", "Gross income", "Taxable income", "Tax credits", "C"),
        ("Which form is used for individual tax returns?", "941", "1099", "W-2", "1040", "D"),
        ("Capital gains are:", "Always taxed at 0%", "Never taxed", "Taxable income", "Exempt", "C"),
        ("A dependent must pass:", "Net worth test", "Support test", "Citizenship test", "Retirement test", "B"),
        ("Which is a refundable credit?", "Child Tax Credit", "SALT deduction", "Mortgage Interest Credit", "Charitable Deduction", "A"),
        ("Business income is reported on:", "Schedule D", "Schedule C", "Schedule E", "Schedule B", "B"),
        ("The IRS stands for:", "Internal Rate Service", "Internal Revenue Service", "Income Report Section", "Income Regulatory System", "B"),
        ("A W-2 form reports:", "Interest income", "Dividend income", "Employment income", "Retirement distributions", "C"),
        ("Which item is not deductible?", "Charitable donations", "Gambling losses exceeding winnings", "Medical expenses", "Property taxes", "B"),
        ("AMT stands for:", "Annual Minimum Tax", "Alternative Minimum Tax", "Applied Marginal Tax", "Aggregate Median Tax", "B")
    ],
    "digital_forensics": [
        ("Digital forensics involves:", "Financial audits", "Evidence recovery from digital devices", "Coding analysis", "Network creation", "B"),
        ("What is chain of custody?", "Chain of emails", "Record of file access", "Documentation of evidence handling", "Backup storage", "C"),
        ("What does a write blocker do?", "Deletes files", "Allows read/write access", "Prevents data modification", "Encrypts files", "C"),
        ("Imaging a disk means:", "Taking screenshots", "Creating an exact copy", "Editing files", "Formatting", "B"),
        ("Metadata includes:", "Binary code", "Visual elements", "File attributes like date created", "Decrypted passwords", "C"),
        ("Volatile data is lost when:", "File is deleted", "Device is shut down", "Hard drive crashes", "RAM is full", "B"),
        ("FTK and EnCase are:", "File formats", "Hardware devices", "Forensic tools", "Legal terms", "C"),
        ("Which is a hashing algorithm?", "SHA-256", "HTML5", "IPsec", "DNS", "A"),
        ("A forensic report should be:", "Technical and vague", "Legal jargon only", "Clear and objective", "Verbal only", "C"),
        ("Data carving is:", "Formatting disks", "Extracting files from raw data", "Backing up logs", "Encrypting partitions", "B")
    ]
}

# Insert all questions
for table, questions in questions_data.items():
    for q in questions:
        cursor.execute(f"""
        INSERT INTO {table} (question, option_a, option_b, option_c, option_d, correct_option)
        VALUES (?, ?, ?, ?, ?, ?)
        """, q)

# Save and close
conn.commit()
conn.close()
print("All tables populated successfully.")
