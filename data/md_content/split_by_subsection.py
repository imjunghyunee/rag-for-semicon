import os
import json
import re
from typing import List, Dict
import tiktoken

# 디렉토리 및 저장 파일 경로
MD_DIR = "./data/md_content"
OUTPUT_JSON = "./data/md_content/subsection_text.json"

# 토크나이저 (GPT-3.5 기준)
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")


def read_markdown_files(directory: str) -> List[str]:
    return [
        os.path.join(directory, fname)
        for fname in os.listdir(directory)
        if fname.endswith(".md")
    ]


def split_by_headers(content: str) -> List[str]:
    """
    '# '와 '## '를 기준으로 텍스트를 청크 단위로 분리하되,
    헤더도 포함한다. '###' 이하 수준은 무시하고 본문에 포함.
    """
    # 제목을 구분자로 포함시켜 분리
    pattern = r"(?=^#\s+.+|^##\s+.+)"  # positive lookahead, 헤더를 포함한 상태로 split
    chunks = re.split(pattern, content, flags=re.MULTILINE)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))


def process_markdown_files():
    all_chunks: List[Dict] = []
    total_tokens = 0
    total_chunks = 0

    md_files = read_markdown_files(MD_DIR)
    for path in md_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        chunks = split_by_headers(content)

        for chunk in chunks:
            token_count = count_tokens(chunk)
            all_chunks.append(
                {
                    "file": os.path.basename(path),
                    "text": chunk,
                    "token_count": token_count,
                }
            )
            total_tokens += token_count
            total_chunks += 1

    # JSON 파일로 저장
    with open(OUTPUT_JSON, "w", encoding="utf-8") as out_f:
        json.dump(all_chunks, out_f, ensure_ascii=False, indent=2)

    # 평균 토큰 수 출력
    if total_chunks > 0:
        average_tokens = total_tokens / total_chunks
        print(f"✅ 총 청크 수: {total_chunks}")
        print(f"✅ 평균 토큰 수: {average_tokens:.2f}")
    else:
        print("⚠️ 처리된 청크가 없습니다.")


if __name__ == "__main__":
    process_markdown_files()
