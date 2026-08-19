# AdI-Psychotherapist-Chatbot
## Build-a-Complete-Mental-Health-Chatbot-with-LLMs-LangChain-Pinecone-Flask

Rationale Behind the Name “AdI Bot”

The nomenclature AdI Bot has been chosen to reflect both technological orientation and personal identity. The term “AdI” originates as a contraction of the developer’s name, Adiba, while simultaneously incorporating AI (Artificial Intelligence), the central foundation of the project. This dual representation establishes a meaningful connection between the creator and the system, offering a personalized dimension to an otherwise technical construct. By embedding individuality into the name, the project emphasizes the human-centered intent behind its design, aligning with the broader objective of leveraging artificial intelligence for empathetic, socially impactful applications in mental health support.

## How to run?
### STEPS:

Clone the repository

```bash
git clone https://github.com/adibaarooj/AdI-Psychotherapist-Chatbot.git
```
(https://github.com/adibaarooj/AdI-Psychotherapist-Chatbot.git)

### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n adibot python=3.10 -y
```

```bash
conda activate adibot
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


### Create a `.env` file in the root directory and add your Pinecone credentials as follows:

```ini
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```


```bash
# run the following command to store embeddings to pinecone
python store_index.py
```

```bash
# Finally run the following command
python app.py
```

Now,
```bash
open up localhost:
```


### Techstack Used:

- Python
- LangChain
- Flask
- Ollama
- Pinecone
