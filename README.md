# Skills

- Python
    - Pandas
    - Matplotlib
    - spaCy
- Git
- GitHub
- Natural language processing
- PowerPoint

# Week 0

- Read the master's thesis provided by Dr Sun

# Week 1

- Met with Dr Sun and Dr Chuan Fu to discuss the project
- Read through Dr Chuan Fu's work to understand his methodology
- Acquired detailed information about different industry classification standards (ICSs) such as ISIC, NACE, SSIC and WZ
- Cleaned the ICS information and standardised columns for a better initial comparison between different standards
- Explored different text preprocessing libraries such as spaCy and NLTK to tokenise the ICS information and obtain the most relevant keywords under each column

# Week 2

- Looked into building a RAG
- Looked at the MAESTRI dataset

Thoughts: 
- Formulate a industry classification table and a resource classification table
    - Use Transformers?
- Manual preprocessing vs. preprocessing using a LLM
- Build a knowledge graph for MAESTRI dataset
    - Use Neo4j

# Week 3

- Worked on validation
- 27 May: Similarity score algorithm is by no means accurate, but Chuan Fu stated that a rough estimation would be sufficient.
- 30 May: Chuan Fu requires an overall metric for the model
- 31 May: Added stacked bar graphs to visualise the accuracy of the model

# Week 4

- TODO: Change the comparison method for ISIC codes such that the respective ISIC code are looked up for a given NACE code.
- TODO: Work on an overall metric of the model
- Added a utilities folder for custom types, constants and functions