# llm_engine.py
import os

PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # "openai", "hf", or "ollama"


def answer_with_llm(context: str, question: str) -> str:
    """
    Answer a question using the selected LLM provider.
    """
    prompt = (
        "Use ONLY the context below to answer the question. "
        "If the answer is not in the context, say 'I don't see enough information in the provided documents.'\n\n"
        f"CONTEXT:\n{context}\n\nQUESTION: {question}\n\n"
        "Answer concisely and cite context where possible."
    )

    if PROVIDER.lower() == "openai":
        return _answer_openai(prompt)
    elif PROVIDER.lower() == "hf":
        return _answer_hf(prompt)
    else:  # default Ollama
        return _answer_ollama(prompt)


def _answer_openai(prompt: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that must use only the provided context."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.0,
        )
        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f"[OpenAI request failed: {e}]"


def _answer_hf(prompt: str) -> str:
    try:
        from transformers import pipeline, set_seed
        gen = pipeline("text-generation", model="distilgpt2")
        set_seed(42)
        out = gen(prompt, max_new_tokens=150, do_sample=True, top_k=50)
        return out[0]["generated_text"]

    except Exception as e:
        return f"[HF generation failed: {e}]"


def _answer_ollama(prompt: str) -> str:
    try:
        import ollama
        response = ollama.chat(
            model=os.getenv("OLLAMA_MODEL", "llama3"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant that must use only the provided context."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["message"]["content"]

    except Exception as e:
        return f"[Ollama request failed: {e}]"
