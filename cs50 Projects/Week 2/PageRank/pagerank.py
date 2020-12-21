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
    trans_mod = {}

    # number of files in corpus
    num_files = len(corpus)

    # get number of links from current page
    num_links = len(corpus[page])

    if num_links != 0 :
        # calculate random probability (which is applicable for all pages)
        rand_prob = (1 - damping_factor) / num_files
        # calculate specific page-related probability
        spec_prob = damping_factor / num_links
    else:
        # calculate random probability (which is applicable for all pages)
        rand_prob = (1 - damping_factor) / num_files
        # calculate specific page-related probability
        spec_prob = 0

    # iterate over files
    for file in corpus:
        # check if current page has any links
        if len(corpus[page]) == 0:
            trans_mod[file] = 1 / num_files
        else:
            # if file is not current page, there is no need to get its links
            if file not in corpus[page]:
                # probability of non-linked page is 1-damp
                trans_mod[file] = rand_prob
            else:
                # probability for linked page is specific plus random probability
                trans_mod[file] = spec_prob + rand_prob
    # check if sum of probabilities is 1
    if round(sum(trans_mod.values()),5) != 1:     # round sum so that 0.99999... will be recognized as 1
        print(f'ERROR! Probabilities add up to {sum(trans_mod.values())}')
    # else:
    #     print(f'\tTransition model probabilities add up to 1: CHECK!')
    return trans_mod
    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    visits = {page_name: 0 for page_name in corpus}

    # First page choice is picked at random:
    curr_page = random.choice(list(visits))
    visits[curr_page] += 1

    # For remaining n-1 samples, pick the page based on the transistion model:
    for i in range(0, n-1):

        trans_model = transition_model(corpus, curr_page, damping_factor)

        # Pick next page based on the transition model probabilities:
        rand_val = random.random()
        total_prob = 0

        for page_name, probability in trans_model.items():
            total_prob += probability
            if rand_val <= total_prob:
                curr_page = page_name
                break

        visits[curr_page] += 1

    # Normalise visits using sample number:
    page_ranks = {page_name: (visit_num/n) for page_name, visit_num in visits.items()}

    print('Sum of sample page ranks: ', round(sum(page_ranks.values()), 4))

    return page_ranks
    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Calculate some constants from the corpus for further use:
    num_pages = len(corpus)
    init_rank = 1 / num_pages
    random_choice_prob = (1 - damping_factor) / len(corpus)
    iterations = 0

    # Initial page_rank gives every page a rank of 1/(num pages in corpus)
    page_ranks = {page_name: init_rank for page_name in corpus}
    new_ranks = {page_name: None for page_name in corpus}
    max_rank_change = init_rank

    # Iteratively calculate page rank until no change > 0.001
    while max_rank_change > 0.001:

        iterations += 1
        max_rank_change = 0

        for page_name in corpus:
            surf_choice_prob = 0
            for other_page in corpus:
                # If other page has no links it picks randomly any corpus page:
                if len(corpus[other_page]) == 0:
                    surf_choice_prob += page_ranks[other_page] * init_rank
                # Else if other_page has a link to page_name, it randomly picks from all links on other_page:
                elif page_name in corpus[other_page]:
                    surf_choice_prob += page_ranks[other_page] / len(corpus[other_page])
            # Calculate new page rank
            new_rank = random_choice_prob + (damping_factor * surf_choice_prob)
            new_ranks[page_name] = new_rank

        # Normalise the new page ranks:
        norm_factor = sum(new_ranks.values())
        new_ranks = {page: (rank / norm_factor) for page, rank in new_ranks.items()}

        # Find max change in page rank:
        for page_name in corpus:
            rank_change = abs(page_ranks[page_name] - new_ranks[page_name])
            if rank_change > max_rank_change:
                max_rank_change = rank_change

        # Update page ranks to the new ranks:
        page_ranks = new_ranks.copy()

    print('Iteration took', iterations, 'iterations to converge')
    print('Sum of iteration page ranks: ', round(sum(page_ranks.values()), 4))

    return page_ranks
    #raise NotImplementedError


if __name__ == "__main__":
    main()
