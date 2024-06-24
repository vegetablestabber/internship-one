# Journal

## Week 0 (06/05/2024 - 10/05/2024)

- Read the master's thesis provided by Dr Sun

## Week 1 (13/05/2024 - 17/05/2024)

- Met with Dr Sun and Dr Chuan Fu to discuss the project
- Read through Dr Chuan Fu's work to understand his methodology
- Acquired detailed information about different industry classification standards (ICSs) such as ISIC, NACE, SSIC and WZ
- Cleaned the ICS information and standardised columns for a better initial comparison between different standards
- Explored different text preprocessing libraries such as spaCy and NLTK to tokenise the ICS information and obtain the most relevant keywords under each column

## Week 2 (20/05/2024 - 24/05/2024)

- Looked into building a RAG
- Looked at the MAESTRI dataset

## Week 3 (27/05/2024 - 31/05/2024)

- Worked on validation
- 27 May: Similarity score algorithm is by no means accurate, but Chuan Fu stated that a rough estimation would be sufficient
- 30 May: Chuan Fu requires an overall metric for the model
- 31 May: Added stacked bar graphs to visualise the accuracy of the model

## Week 4 (03/06/2024 - 07/06/2024)

- Added a utilities folder for custom types, constants and functions

## Week 5 (10/06/2024 - 14/06/2024)

- TODO: Change the comparison method for ISIC codes such that the respective ISIC code are looked up for a given NACE code.
- TODO: Work on an overall metric of the model
- TODO: Add Jupyter notebooks to the 'notebooks' folder

### Meeting minutes

- Improve the scoring algorithm (i.e. similarity threshold score)
- LLMs can be used to improve the matching, but it will be computationally (and time) intensive
- Need a labelled dataset so that it can be used it for making predictions
- Use ChatGPT as opposed to using a LLM locally
- We could also generate examples using a LLM to increase the matching accuracy

## Week 6 (18/06/2024 - 21/06/2024)

### Goals before meeting supervisors

- Improve accuracy of the correspondence tables
- Use Llama 3 to get better matches from Chuan Fu's correspondence tables for the MAESTRI dataset
- Labelled dataset
    = How do I make a labelled dataset?
        - MAESTRI dataset: Company code, company keywords
        - Correspondence table: Given code, possible codes
    - How can someone use this labelled dataset?
        - Find similar keywords

## Week 7 (24/06/2024 - 28/06/2024)

## Week 8 (01/07/2024 - 05/07/2024)

## Week 9 (08/07/2024 - 12/07/2024)

## Week 10 (15/07/2024 - 19/07/2024)

## Week 11 (22/07/2024 - 26/07/2024)

## Week 10 (29/07/2024 - 02/08/2024)