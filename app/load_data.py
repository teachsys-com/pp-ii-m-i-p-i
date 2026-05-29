import os
import tempfile
import pandas as pd
import requests
from database import SessionLocal, engine
from models import Base, Question

# Public QA Dataset from HuggingFace (SQuAD Validation Parquet Shard)
DATASET_URL = "https://huggingface.co/datasets/rajpurkar/squad/resolve/refs%2Fconvert%2Fparquet/plain_text/validation/0000.parquet"


def download_parquet(url: str) -> str:
    print(f"Descargando {url}...")
    r = requests.get(url, stream=True)
    r.raise_for_status()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".parquet")
    tmp.write(r.content)
    tmp.close()
    return tmp.name


def parse_squad_answer(answers_dict) -> str:
    if isinstance(answers_dict, dict):
        texts = answers_dict.get("text")
        if texts is not None and len(texts) > 0:
            return texts[0]
    elif hasattr(answers_dict, "get"):
        texts = answers_dict.get("text")
        if texts and len(texts) > 0:
            return texts[0]
    return ""


def load_questions():
    # Make sure tables are created
    Base.metadata.create_all(bind=engine)

    parquet_path = download_parquet(DATASET_URL)
    try:
        df = pd.read_parquet(parquet_path)
    finally:
        if os.path.exists(parquet_path):
            os.unlink(parquet_path)

    print(f"Columnas disponibles: {list(df.columns)}")
    print(f"Filas totales: {len(df)}")
    print(df.head(3))

    session = SessionLocal()
    try:
        # Ingest first 100 questions for demonstration to keep it quick
        df_slice = df.head(100)
        inserted_count = 0
        for _, row in df_slice.iterrows():
            answer_text = parse_squad_answer(row.get("answers"))

            question = Question(
                question=row.get("question", ""),
                answer=answer_text,
                category=row.get("title", ""),
                source="HuggingFace - rajpurkar/squad (validation)",
            )
            session.add(question)

        session.commit()
        print(f"Se insertaron {len(df_slice)} preguntas correctamente.")
    except Exception as e:
        session.rollback()
        print(f"Error durante la carga: {e}")
        raise e
    finally:
        session.close()


if __name__ == "__main__":
    load_questions()
