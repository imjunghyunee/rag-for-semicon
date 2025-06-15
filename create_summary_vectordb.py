import json
import os
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer
import torch
from pathlib import Path

def main():
    # 1. 데이터 파일 경로 설정
    data_file = "./data/examples_text_summary_pair.json"
    
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file not found: {data_file}")
    
    # 2. JSON 데이터 로드
    print(f"Loading data from {data_file}...")
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} examples from JSON file")
      # 3. summary 텍스트만 추출하여 Document 객체 생성
    documents = []
    for idx, item in enumerate(data):
        if "summary" not in item:
            print(f"Warning: Item {idx} missing 'summary' field, skipping...")
            continue
        
        summary_text = item["summary"]
        
        # metadata 구성 - parent_id는 examples_original.jsonl에서 찾을 수 있는 식별자여야 함
        metadata = {
            "source": "examples_text_summary_pair.json",
            "index": idx,
            "parent_id": str(idx),  # examples_original.jsonl의 id와 매칭되도록 설정
        }
        
        # id 값이 있으면 metadata에 추가 (Example 1.1, Example 1.2 등)
        if "id" in item:
            example_id = item["id"]
            metadata["example_id"] = example_id
            # parent_id를 example_id 기반으로 설정 (retrievers.py에서 이 값으로 검색)
            metadata["parent_id"] = example_id
        
        # original 텍스트도 있으면 길이 정보 추가 (검색 결과 분석에 유용)
        if "original" in item:
            metadata["original_length"] = len(item["original"])
        
        doc = Document(
            page_content=summary_text,
            metadata=metadata
        )
        documents.append(doc)
    
    print(f"Created {len(documents)} Document objects from summaries")
    
    # 문서 확인 (처음 3개 출력)
    for idx, doc in enumerate(documents[:3]):
        print(f"\nDocument {idx + 1}:")
        print(f"Content: {doc.page_content[:100]}...")
        print(f"Metadata: {doc.metadata}")
        print("=" * 50)
    
    # 4. HuggingFace 임베딩 모델 정의 (기존 create_vectordb.py와 동일)
    print("Loading embedding model...")
    embedding_model = HuggingFaceEmbeddings(
        model_name="jinaai/jina-embeddings-v3",
        model_kwargs={
            "trust_remote_code": True,
            "device": "cuda" if torch.cuda.is_available() else "cpu",
        },
        encode_kwargs={"normalize_embeddings": True},
    )
    print(f"Embedding model loaded on {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    
    # 5. FAISS vector DB 생성
    print("Creating FAISS vector database...")
    vectordb = FAISS.from_documents(documents, embedding_model)
    
    # 6. 저장 디렉토리 생성 및 저장
    save_path = "./vectordb/summary_faiss"
    os.makedirs(save_path, exist_ok=True)
    
    vectordb.save_local(save_path)
    print(f"Successfully created and saved the summary FAISS vector database at {save_path}")
    
    # 7. 토큰 수 계산 및 분석 (선택적)
    print("Analyzing token statistics...")
    try:
        tokenizer = AutoTokenizer.from_pretrained("jinaai/jina-embeddings-v3", trust_remote_code=True)
        
        token_info = []
        token_counts = []
        
        for idx, doc in enumerate(documents):
            tokens = tokenizer.encode(doc.page_content, add_special_tokens=False)
            token_count = len(tokens)
            token_counts.append(token_count)
            
            chunk_data = {
                "index": idx,
                "example_id": doc.metadata.get("example_id", f"Unknown_{idx}"),
                "token_count": token_count,
                "text_length": len(doc.page_content),
                "summary_text": doc.page_content,
                "metadata": doc.metadata,
            }
            token_info.append(chunk_data)
        
        # 8. 통계 출력
        avg_tokens = sum(token_counts) / len(token_counts) if token_counts else 0
        min_tokens = min(token_counts) if token_counts else 0
        max_tokens = max(token_counts) if token_counts else 0
        
        print(f"\n📊 Summary Vector Database Statistics:")
        print(f"  - Total documents: {len(documents)}")
        print(f"  - Average tokens per summary: {avg_tokens:.2f}")
        print(f"  - Min tokens: {min_tokens}")
        print(f"  - Max tokens: {max_tokens}")
        
        # 9. JSON 파일로 토큰 정보 저장
        json_save_path = "./vectordb/summary_token_info.json"
        with open(json_save_path, "w", encoding="utf-8") as f:
            json.dump(token_info, f, indent=2, ensure_ascii=False)
        
        print(f"📝 Summary token info saved to {json_save_path}")
        
    except Exception as e:
        print(f"Warning: Could not analyze tokens: {e}")
    
    # 10. 검증: 로드 테스트
    print("\n🔍 Verification: Testing database load...")
    try:
        test_vectordb = FAISS.load_local(
            save_path,
            embeddings=embedding_model,
            allow_dangerous_deserialization=True,
        )
        
        # 간단한 검색 테스트
        test_query = "calculate crystal structure"
        test_results = test_vectordb.similarity_search(test_query, k=2)
        
        print(f"✅ Database load test successful!")
        print(f"✅ Test search for '{test_query}' returned {len(test_results)} results")
        
        if test_results:
            print(f"✅ First result metadata: {test_results[0].metadata}")
        
    except Exception as e:
        print(f"❌ Database load test failed: {e}")
    
    print(f"\n🎉 Summary vector database creation completed!")
    print(f"📁 Database saved at: {save_path}")
    print(f"📄 Token analysis saved at: ./vectordb/summary_token_info.json")


if __name__ == "__main__":
    main()
