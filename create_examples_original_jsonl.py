import json
import os
from pathlib import Path

def create_examples_original_jsonl():
    """
    examples_text_summary_pair.json에서 original 데이터를 추출하여
    retrievers.py에서 사용할 수 있는 examples_original.jsonl 파일을 생성합니다.
    """
    
    # 1. 입력 파일 경로
    input_file = "./data/examples_text_summary_pair.json"
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # 2. 출력 디렉토리 및 파일 경로 설정
    output_dir = Path("./vectordb/jina_processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "examples_original.jsonl"
    
    # 3. JSON 데이터 로드
    print(f"Loading data from {input_file}...")
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} examples from JSON file")
    
    # 4. JSONL 파일로 변환하여 저장
    print(f"Creating {output_file}...")
    
    with open(output_file, "w", encoding="utf-8") as f:
        for idx, item in enumerate(data):
            # retrievers.py에서 기대하는 형태로 데이터 구성
            jsonl_record = {
                "id": item.get("id", f"example_{idx}"),  # Example 1.1, Example 1.2 등
                "page_content": item.get("original", ""),  # original 텍스트가 실제 컨텍스트
                "metadata": {
                    "source": "examples_text_summary_pair.json",
                    "index": idx,
                    "example_id": item.get("id", f"example_{idx}"),
                    "has_summary": "summary" in item,
                    "original_length": len(item.get("original", "")),
                    "summary_length": len(item.get("summary", "")) if "summary" in item else 0,
                }
            }
            
            # JSONL 형태로 한 줄씩 저장
            f.write(json.dumps(jsonl_record, ensure_ascii=False) + "\n")
    
    print(f"✅ Successfully created {output_file}")
    print(f"📊 Total records: {len(data)}")
    
    # 5. 검증: 파일 읽기 테스트
    print("\n🔍 Verification: Testing file reading...")
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        print(f"✅ File reading test successful! {len(lines)} lines found")
        
        # 첫 번째 레코드 출력
        if lines:
            first_record = json.loads(lines[0])
            print(f"✅ First record ID: {first_record['id']}")
            print(f"✅ First record content preview: {first_record['page_content'][:100]}...")
            
    except Exception as e:
        print(f"❌ File reading test failed: {e}")

if __name__ == "__main__":
    create_examples_original_jsonl()
