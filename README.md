<h1 align="center"> RealEstateAI: Your Intelligent Real Estate Assistant 🏠 </h1>
<p align="center">
  Samar Samara, Kinan ibraheem, Rawan Badarneh
  <p align="center">
    Technion
  </p>
</p>

RealEstateAI is an intelligent real estate search assistant that helps users find properties that match their specific needs using AI-driven recommendations. By analyzing market data, location trends, and user preferences, RealEstateAI provides personalized property suggestions and insights to optimize real estate decisions.

## 🌟 Key Features

### Intelligent Property Matching
- **Natural Language Understanding**: Simply describe your dream home in plain English
- **Semantic Search Engine**: Powered by Qdrant for intelligent property matching
- **Personalized Recommendations**: Tailored suggestions based on your unique preferences
- **Dynamic Property Descriptions**: AI-generated, engaging property descriptions that highlight relevant features

### Advanced Technology Stack
- **LangChain Integration**: Seamless combination of language models and document retrieval
- **Vector Database**: Qdrant for efficient similarity search and property matching
- **GPT-4o Language Model**: State-of-the-art natural language processing

### Data Management
- **Data Source**: Houses that were sold in California in 2020. 
- **Structured Property Information**: Comprehensive property details including:
  - Property specifications (size, bedrooms, bathrooms)
  - Amenities (schools, schools score)
  - Price points
  - Property descriptions
 

## 🚀 Getting Started

### Prerequisites
- Python 3.11 
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/samarsamara/RealEstateAI.git
cd RealEstateAI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create ".env" file that contains your OpenAI API key:
   ```
   API_KEY=<your_api_key>
   ``` 

### Running the Application

Launch the application:
```bash
python RealEstateAI.py
```

## 📦 Project Structure
```
RealEstateAI/
│── examples/
│   ├── example1.txt
│   ├── example2.txt
│   ├── example3.txt
│   ├── example4.txt
│   ├── example5.txt
├── Data/
│   ├── los_angeles.csv
├── Code/
│   ├── RealEstateAI.py      # Main application script
│   ├── create_VDBs.py       # create the vector data base
│   ├── create_embeddings.py       # create the embedding for each data raw
│   ├── exploring_agent.py      # Agentic RAG
│   ├── interacting_agent.py    # conversation manager 
│   ├── recommendation_agent.py       # return the final recommendation for the user
├── requirements.txt          # Project dependencies
└── README.md                # Project documentation
```

## 💻 Technical Details

### Dependencies
```
qdrant-client
tiktoken
numpy
pandas
torch
transformers
faiss-cpu
sentence-transformers
tqdm
langchain_openai
json
os
langchain

```



## 🎯 Example Usage

1. Start the application.
2. Enter your preferences in natural language:
   - "I'm looking for a 3-bedroom house in Beverly Hills with budget 1m"
   - "I want a condo with 2-bedroom and one bathroom apartment in los angeles with a budget of $500K"
3. View personalized recommendations with property descriptions.



## App Architecture:

![Alt Text](https://github.com/samarsamara/RealEstateAI/blob/main/Image20250308195141.jpg)



## Notes :
1. Our AI agent exclusively **searches for properties in Los Angeles**, requiring users to input their **budget, number of bedrooms, and number of bathrooms** as mandatory criteria.
2. Link for the embedded data : https://drive.google.com/drive/folders/1bsPUZ-zUZCfAebIkm2s_D-fPxOXQSVx9?usp=sharing.
   
