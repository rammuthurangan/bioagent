from agents.blast_agent import blast_agent
from agents.pubmed_agent import pubmed_agent

# Test protein sequence - this is human insulin
test_sequence = "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"

print("🧬 BioAgent Multi-Agent Analysis")
print("=" * 50)

# Step 1 - BLAST Analysis
print("\n🔍 Step 1: Running BLAST analysis...")
blast_results = blast_agent(test_sequence, sequence_type="protein")

print("\nTop BLAST Hits:")
print("-" * 30)
for i, hit in enumerate(blast_results["hits"][:3], 1):
    print(f"{i}. {hit['title'][:80]}")
    print(f"   Identity: {hit['identity_percent']}% | E-value: {hit['evalue']}")

# Step 2 - Literature Search
print("\n📚 Step 2: Searching scientific literature...")
literature_results = pubmed_agent(blast_results["hits"])

print(f"\nFound {len(literature_results['papers'])} relevant papers:")
print("-" * 40)
for i, paper in enumerate(literature_results["papers"], 1):
    print(f"{i}. {paper['title'][:100]}")
    print(f"   Journal: {paper['journal']}")
    print(f"   PMID: {paper['pmid']}")

# Step 3 - Combined Analysis
print("\n🤖 Combined AI Analysis:")
print("=" * 50)
print("\nBLAST Interpretation:")
print("-" * 20)
print(blast_results["interpretation"])

print("\nLiterature Summary:")
print("-" * 20)
print(literature_results["summary"])

print("\n✅ Analysis Complete!")