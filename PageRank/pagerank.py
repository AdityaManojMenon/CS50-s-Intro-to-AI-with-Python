import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = {}
    links = corpus[page]
    num_links = len(links)
    num_pages = len(corpus)

    if num_links == 0:
        for x in corpus:
            probability_distribution[x] = 1/num_pages
    else:
        for x in corpus:
            probability_distribution[x] = (1 - damping_factor)/num_pages
        for link in links:
            probability_distribution[link] += damping_factor/num_links

    return probability_distribution 


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {page: 0 for page in corpus}
    
    current_page = random.choice(list(corpus.keys()))
    
    for _ in range(n):
        page_rank[current_page] += 1
        model = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(model.keys()), list(model.values()))[0]
    
    for page in page_rank:
        page_rank[page] /= n
    
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    page_rank = {page: 1 / num_pages for page in corpus}
    new_page_rank = page_rank.copy()
    
    while True:
        for page in corpus:
            total = 0
            for potential_linker in corpus:
                if page in corpus[potential_linker]:
                    total += page_rank[potential_linker] / len(corpus[potential_linker])
                if len(corpus[potential_linker]) == 0:
                    total += page_rank[potential_linker] / num_pages
            new_page_rank[page] = (1 - damping_factor) / num_pages + damping_factor * total
        
        # Check for convergence
        if all(abs(new_page_rank[page] - page_rank[page]) < 0.001 for page in page_rank):
            break
        page_rank = new_page_rank.copy()
    
    return new_page_rank

if __name__ == "__main__":
    main()
