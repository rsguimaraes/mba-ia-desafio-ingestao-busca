from search import search_prompt
from dotenv import load_dotenv
from vector_store import get_vector_store, validate_envs

def execute():
    print("Digite SAIR para encerrar o programa.")

    while True:
        question = input("Faça sua pergunta: ").strip()

        if question.upper() == "SAIR":
            break

        if not question:
            print("Erro: a pergunta não pode ser vazia.")
        else:
            search(question)

def semantic_search(question: str):
    store = get_vector_store()
    results = store.similarity_search_with_score(question, k=10)
    return results

def llm_search(question: str, results):
    chain = search_prompt()
    contexto = "\n\n".join(doc.page_content for doc, _ in results)
    resposta = chain.invoke({"contexto": contexto, "pergunta": question})
    print(resposta)

def search(question: str):
    results = semantic_search(question)
    llm_search(question, results)


load_dotenv() 
validate_envs()

if __name__ == "__main__":
    execute()