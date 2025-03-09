import os
import pandas as pd
from tqdm import tqdm
from langchain_openai.embeddings import AzureOpenAIEmbeddings

def load_env_file(filepath=".env"):
    """
    Load key-value pairs from a .env file into environment variables.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} does not exist.")

    with open(filepath, "r") as file:
        for line in file:
            # Ignore empty lines and comments
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key] = value.strip()

def get_azure_embeddings(text, api_key):
    """
    Extract embeddings using Azure OpenAI and LangChain.
    """
    embeddings = AzureOpenAIEmbeddings(
        model="team6-embedding",  # Replace with your Azure deployment name
        azure_endpoint="https://096290-oai.openai.azure.com",
        openai_api_key=api_key,
        openai_api_version="2023-05-15",
    )
    # Get embeddings for the input text
    return embeddings.embed_query(text)

def format_key_value_text(row):
    """
    Converts a DataFrame row into a structured text format: "Key: Value".
    If a value is empty or NaN, it remains empty after the colon.
    """
    return ", ".join([f"{col}: {row[col]}" for col in row.index])

if __name__ == "__main__":
    # Load the CSV file
    df = pd.read_csv("los_angeles.csv")

    df = df.drop(['Address', 'Zip'], axis=1)
    #applying transformations to the data
    df['Heating'] = df['Heating'].fillna('No')
    df['Cooling'] = df['Cooling'].fillna('No')
    df['Parking'] = df['Parking'].fillna('No')

    df['Heating'] = df['Heating'].apply(lambda x: 'Yes' if x != 'No' else x)
    df['Cooling'] = df['Cooling'].apply(lambda x: 'Yes' if x != 'No' else x)
    df['Parking'] = df['Parking'].apply(lambda x: 'Yes' if x != 'No' else x)

    df['joined_text'] = df.apply(format_key_value_text, axis=1)
    df.reset_index(inplace=True)

    # Load environment variables and API key
    load_env_file()
    api_key = os.getenv("API_KEY")

    embeddings_list = []
    # Compute embeddings for each text
    for text in tqdm(df['joined_text'], desc="Extracting Embeddings"):
        embedding = get_azure_embeddings(text, api_key)
        embeddings_list.append(embedding)

    df['embeddings'] = embeddings_list

    # Save the DataFrame to a Parquet file
    df[['index', 'embeddings']].to_parquet("los_angeles_embeddings_final.parquet", index=False, engine="pyarrow")
    print("Embeddings saved to 'los_angeles_embeddings_final.parquet'")
