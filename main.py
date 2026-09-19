import pandas as pd

# Load datasets
tickets = pd.read_csv("data/support_tickets_10k.csv")
faqs = pd.read_csv("data/faq_knowledge_base_150.csv")

# -------------------------
# Ticket Dataset
# -------------------------

print("===== TICKET DATASET =====")

print("Shape:", tickets.shape)

print("\nColumns:")
print(tickets.columns.tolist())

print("\nFirst 5 records:")
print(tickets.head())

print("\nMissing values:")
print(tickets.isnull().sum())

print("\nTicket Categories:")
print(tickets["ticket_category"].value_counts())

print("\nPriorities:")
print(tickets["priority"].value_counts())

print("\nSentiments:")
print(tickets["sentiment"].value_counts())


# -------------------------
# FAQ Dataset
# -------------------------

print("\n\n===== FAQ DATASET =====")

print("Shape:", faqs.shape)

print("\nColumns:")
print(faqs.columns.tolist())

print("\nFirst 5 records:")
print(faqs.head())

print("\nMissing values:")
print(faqs.isnull().sum())

print("\nFAQ Categories:")
print(faqs["category"].value_counts())