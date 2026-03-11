from Bio import Entrez
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Set your email for Entrez (required by NCBI)
Entrez.email = "your_email@example.com"  # Replace with your real email
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def search_pubmed(search_term, max_results=5):
    """
    Search PubMed for papers related to a search term
    """
    print(f"Searching PubMed for: {search_term}")
    
    try:
        # Search PubMed
        handle = Entrez.esearch(db="pubmed", term=search_term, retmax=max_results)
        search_results = Entrez.read(handle)
        handle.close()
        
        # Get the paper IDs
        paper_ids = search_results["IdList"]
        
        if not paper_ids:
            return []
        
        # Fetch paper details
        handle = Entrez.efetch(db="pubmed", id=paper_ids, rettype="medline", retmode="text")
        papers = handle.read()
        handle.close()
        
        # Parse papers into a cleaner format
        return parse_pubmed_results(papers, paper_ids)
        
    except Exception as e:
        print(f"PubMed search error: {e}")
        return []

def parse_pubmed_results(papers_text, paper_ids):
    """
    Parse the raw PubMed results into structured data
    """
    papers = []
    lines = papers_text.strip().split('\n')
    
    current_paper = {}
    current_field = None
    
    for line in lines:
        if line.startswith('PMID- '):
            # Start of new paper
            if current_paper:
                papers.append(current_paper)
            current_paper = {
                'pmid': line.replace('PMID- ', '').strip(),
                'title': '',
                'abstract': '',
                'authors': '',
                'journal': ''
            }
        elif line.startswith('TI  - '):
            current_paper['title'] = line.replace('TI  - ', '').strip()
            current_field = 'title'
        elif line.startswith('AB  - '):
            current_paper['abstract'] = line.replace('AB  - ', '').strip()
            current_field = 'abstract'
        elif line.startswith('AU  - '):
            if current_paper['authors']:
                current_paper['authors'] += ', '
            current_paper['authors'] += line.replace('AU  - ', '').strip()
        elif line.startswith('JT  - '):
            current_paper['journal'] = line.replace('JT  - ', '').strip()
        elif line.startswith('      ') and current_field:
            # Continuation of previous field
            if current_field == 'title':
                current_paper['title'] += ' ' + line.strip()
            elif current_field == 'abstract':
                current_paper['abstract'] += ' ' + line.strip()
    
    # Add the last paper
    if current_paper:
        papers.append(current_paper)
    
    return papers

def pubmed_agent(blast_hits, max_papers=3):
    """
    Agent that searches PubMed based on BLAST hits and summarizes findings
    """
    if not blast_hits:
        return {"papers": [], "summary": "No BLAST hits to search literature for."}
    
    # Extract search terms from top BLAST hits
    search_terms = []
    for hit in blast_hits[:2]:  # Use top 2 hits
        title = hit['title'].lower()
        # Extract meaningful protein/gene names
        if 'insulin' in title:
            search_terms.append('insulin')
        elif 'actin' in title:
            search_terms.append('actin')
        elif 'rubisco' in title:
            search_terms.append('RuBisCO')
        # Add more protein patterns as needed
        
        # Generic approach - extract first meaningful word
        words = title.split()
        for word in words:
            if len(word) > 4 and word.isalpha():
                search_terms.append(word)
                break
    
    if not search_terms:
        search_terms = ['protein structure function']
    
    # Search PubMed for each term
    all_papers = []
    for term in search_terms[:2]:  # Limit to avoid too many API calls
        papers = search_pubmed(term, max_results=max_papers)
        all_papers.extend(papers)
    
    # Remove duplicates
    seen_pmids = set()
    unique_papers = []
    for paper in all_papers:
        if paper['pmid'] not in seen_pmids:
            unique_papers.append(paper)
            seen_pmids.add(paper['pmid'])
    
    # Limit total papers
    unique_papers = unique_papers[:max_papers]
    
    # Generate AI summary of literature findings
    if unique_papers:
        literature_text = ""
        for i, paper in enumerate(unique_papers, 1):
            literature_text += f"""
Paper {i}:
Title: {paper['title']}
Journal: {paper['journal']}
Abstract: {paper['abstract'][:500]}...
"""

        prompt = f"""
Based on these recent scientific papers, provide insights about the protein/sequence we identified from BLAST:

{literature_text}

Please summarize:
1. Key recent findings about this protein's function
2. Current research directions
3. Any clinical or therapeutic relevance
4. How this literature supports or expands on our BLAST identification

Keep it concise and focused on the most important scientific insights.
"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert bioinformatician summarizing recent literature to support sequence analysis findings."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.3
        )
        
        summary = response.choices[0].message.content
    else:
        summary = "No relevant recent papers found in PubMed."
    
    return {
        "papers": unique_papers,
        "search_terms": search_terms,
        "summary": summary
    }