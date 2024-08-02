# Requirements

- `spacy==3.7.4`
    - This project uses the default [spaCy](https://spacy.io) trained pipeline `en_core_web_trf`. You may also use other pipelines mentioned [here](https://spacy.io/usage/models).
    - To use this pipeline on your machine:
        1. Install spaCy: `pip install spaCy`
        2. Download the pipeline: `python -m spacy download 
- `ollama==0.2.1`
    - This project runs [Llama 3](https://llama.meta.com) via [Ollama](https://ollama.com). You can browse other supported models [here](https://ollama.com).
    - To download the model to your machine:
        1. Install Ollama: `pip install ollama`
        2. Download Llama 3: `ollama pull llama3`
en_core_web_trf`
- `autocorrect==2.6.1`
- `xlsxwriter==3.2.0`
- `matplotlib==3.9.0`
- `pandas==2.2.2`
- `numpy==1.26.4`
- `tqdm==4.66.4`

You can also copy the commands below to install the pre-requisites after cloning this project:

```
pip install -r requirements.txt
python -m spacy download en_core_web_trf
ollama pull llama3
```

# Usage

1. First, run `notebooks/clean_inference.ipynb` to generate formatted classification inference files within the `exports` folder.
2. To validate the preliminary results of matching industry classifications within the MAESTRI dataset by Dr Tan Chuan Fun, run `notebooks/validate_maestri.ipynb`.
3. To validate the results from the new methodology implemented in this project, run `notebooks/match_maestri.ipynb`.

# Data

## Industrial symbiosis datasets

- [MAESTRI](https://maestri-spire.eu/)

## Industry classification standard inference tables

- [ISIC Revision 4](https://unstats.un.org/unsd/classifications/Econ/isic)
- [NACE Revision 2](/data/inference/industry/NACE%20Rev.%202.xlsx)
- [WZ Issue 2008](https://www.klassifikationsserver.de/klassService/jsp/common/url.jsf?variant=wz2008&lang=EN)
- [SSIC 2020](https://www.singstat.gov.sg/standards/standards-and-classifications/ssic)

# Resources

## Textbooks

- [Practical Natural Language Processing](https://www.oreilly.com/library/view/practical-natural-language/9781492054047/)