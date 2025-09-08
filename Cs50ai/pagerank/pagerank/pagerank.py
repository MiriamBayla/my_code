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
    distribution = {}
    links = corpus[page]
    total_pages = len(corpus)

    # If the given page does have links in it
    if links:
        # for every page in the corpus
        for p in corpus:
            # when user is bored and goes to random page
            distribution[p] = (1 - damping_factor) / len(corpus)
            # If user goes to linked page
            if p in links:
                distribution[p] += damping_factor / len(links)

    # If the given page does not have links in it
    else:
        for p in corpus:
            distribution[p] = 1 / len(corpus)
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    visits = {}
    for page in corpus:
        visits[page] = 0
    # Get random page as first sample
    sample = random.choice(list(corpus.keys()))

    # Check n amount of sampless=
    for _ in range(n):
        visits[sample] += 1
        # Find pages' weights
        likelihood = transition_model(corpus, sample, damping_factor)
        # Randomly choose a page while giving weight to pages which are more likely to be chosen
        sample = random.choices(
            population=list(likelihood.keys()),
            weights=list(likelihood.values()),
            k=1)[0]

    # Turn from the amount of visits per page to it's likelihood to be chosen out of all samples
    ranks = {}
    for visit in visits:
        ranks[visit] = visits[visit] / n

    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    converged = False
    ranks = {}
    # Initialize ranks to 1/number of pages
    N = len(corpus)
    for page in corpus:
        ranks[page] = 1 / N

    while not converged:
        new_ranks = {}
        converged = True

        for page in corpus:
            # Likelihood of randomly starting at this page
            new_rank = (1 - damping_factor) / N

            # What's its rank based on number of links leading to this page
            # Its importance of being linked to by other pages starts at 0
            total = 0
            for maybe_linking in corpus:

                # If maybe_linking page links to page we're checking
                if page in corpus[maybe_linking]:
                    # Add to the page we're checking's total value the value of the linking page, divide by num of links in it
                    total += ranks[maybe_linking] / len(corpus[maybe_linking])

                # If maybe_linking page has no links - treat as if it links to all pages
                if not corpus[maybe_linking]:
                    total += ranks[maybe_linking] / N

            # Add the damping factor to the total sum
            new_rank = total * damping_factor + (1 - damping_factor) / N

            # Update the new ranks dictionary with this page's new rank
            new_ranks[page] = new_rank

        # Check if ranks' values are close enough to new_ranks' (and therefore their converged...)
        for page in corpus:
            if abs(ranks[page] - new_ranks[page]) > 0.001:
                converged = False

        ranks = new_ranks

    return ranks


if __name__ == "__main__":
    main()
