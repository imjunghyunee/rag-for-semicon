from __future__ import annotations
from typing import List, Dict, Any, Optional
from rag_pipeline import utils, retrievers, config
from langchain.schema import Document


def decompose_query(original_query: str, max_subquestions: int = 5) -> List[str]:
    """
    복잡한 질문을 더 작은 하위 질문들로 분해합니다.

    Args:
        original_query: 원본 복잡한 질문
        max_subquestions: 최대 하위 질문 개수

    Returns:
        하위 질문들의 리스트
    """
    try:
        response = utils.client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an expert in semiconductor physics who excels at breaking down complex questions into simpler, manageable sub-questions.

                                    When given a complex question, break it down into {max_subquestions} or fewer sub-questions that:
                                    1. Are simpler and more focused than the original question
                                    2. Build upon each other logically
                                    3. When answered together, provide comprehensive information to solve the original question
                                    4. Are specific to semiconductor physics domain

                                    Examples of good decomposition:
                                    - Complex: "How does temperature affect both carrier concentration and mobility in silicon devices?"
                                    - Sub-questions:
                                    1. What is the relationship between temperature and intrinsic carrier concentration in silicon?
                                    2. How does temperature affect electron and hole mobility in silicon?
                                    3. What are the combined effects on device performance?

                                    Format your response as a numbered list:
                                    1. [First sub-question]
                                    2. [Second sub-question]
                                    ...

                                    Respond with ONLY the numbered list of sub-questions.""",
                },
                {
                    "role": "user",
                    "content": f"Let's break down this complex semiconductor physics question: {original_query}",
                },
            ],
            max_tokens=5000,
            temperature=0.3,
        )

        response_text = response.choices[0].message.content.strip()

        # Parse numbered list into individual questions
        subquestions = []
        lines = response_text.split("\n")

        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                # Remove numbering and clean up
                if ". " in line:
                    question = line.split(". ", 1)[1].strip()
                elif "- " in line:
                    question = line.split("- ", 1)[1].strip()
                else:
                    question = line.strip()

                if question and len(question) > 10:  # Filter out very short responses
                    subquestions.append(question)

        # Fallback if no valid sub-questions generated
        if not subquestions:
            print(
                "Warning: No valid sub-questions generated, creating fallback questions"
            )
            # Simple fallback strategy
            subquestions = [
                f"What are the fundamental concepts related to: {original_query}?",
                f"What are the key factors that influence: {original_query}?",
                f"How can we analyze or solve: {original_query}?",
            ]

        # Limit to max_subquestions
        return subquestions[:max_subquestions]

    except Exception as e:
        print(f"Error in query decomposition: {e}")
        # Return fallback questions
        return [
            f"What are the basic principles underlying this question: {original_query}?",
            f"What specific factors should be considered for: {original_query}?",
        ]


def process_subquestion(
    subquestion: str,
    retrieval_type: Optional[str] = None,
    hybrid_weights: Optional[List[float]] = None,
    previous_results: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    하위 질문에 대해 검색 및 답변 생성을 수행합니다.
    이전 단계의 질문-답변 컨텍스트를 포함하여 순차적으로 처리합니다.

    Args:
        subquestion: 처리할 하위 질문
        retrieval_type: 검색 타입 (hyde, summary, summary_mean, None)
        hybrid_weights: 하이브리드 검색 가중치
        previous_results: 이전 단계들의 처리 결과 리스트

    Returns:
        검색된 컨텍스트와 답변을 포함한 딕셔너리
    """
    current_step = len(previous_results) + 1 if previous_results else 1
    print(f"   Processing Step {current_step} subquestion: {subquestion}")
    
    # 1) 검색 타입에 따라 적절한 검색 함수 선택
    if retrieval_type == "hyde" and hybrid_weights:
        context_docs, explanation = retrievers.hyde_hybrid_retrieve(
            subquestion, weights=hybrid_weights
        )
    elif retrieval_type == "hyde":
        context_docs, explanation = retrievers.hyde_retrieve(subquestion)
    elif retrieval_type == "summary" and hybrid_weights:
        context_docs, explanation = retrievers.summary_hybrid_retrieve(
            subquestion, weights=hybrid_weights
        )
    elif retrieval_type == "summary":
        context_docs, explanation = retrievers.summary_retrieve(subquestion)
    elif retrieval_type == "summary_mean" and hybrid_weights:
        context_docs, explanation = retrievers.summary_mean_retrieve_hybrid(
            subquestion, weights=hybrid_weights
        )
    elif retrieval_type == "summary_mean":
        context_docs, explanation = retrievers.summary_mean_retrieve(subquestion)
    elif hybrid_weights:
        context_docs = retrievers.vectordb_hybrid_retrieve(
            subquestion, weights=hybrid_weights
        )
        explanation = ""
    else:
        context_docs = retrievers.vectordb_retrieve(subquestion)
        explanation = ""

    # 2) 컨텍스트 문서들을 문자열로 변환
    if isinstance(context_docs, tuple):
        context_docs = context_docs[0]  # tuple인 경우 첫 번째 요소가 문서들

    context_contents = [
        doc.page_content for doc in context_docs if isinstance(doc, Document)
    ]
    retrieved_context = "\n\n---\n\n".join(context_contents)

    # 3) 이전 단계들의 Q&A 컨텍스트 구성 (요구사항 2 핵심 부분)
    previous_qa_contexts = []
    if previous_results:
        for i, result in enumerate(previous_results, 1):
            # 각 이전 단계의 Q&A를 명확히 구조화
            qa_pair = f"=== Step {i} ===\nQuestion: {result['question']}\nAnswer: {result['answer']}"
            previous_qa_contexts.append(qa_pair)
        
        print(f"   📚 Including Q&A context from {len(previous_results)} previous steps")
    
    previous_qa_context = "\n\n".join(previous_qa_contexts)

    # 4) 전체 컨텍스트 구성: 이전 Q&A + 현재 검색된 문서들 (요구사항 2 구현)
    context_sections = []
    
    if previous_qa_context:
        context_sections.append(f"=== Previous Steps Q&A ===\n{previous_qa_context}")
    
    if retrieved_context:
        context_sections.append(f"=== Step {current_step} Retrieved Documents ===\n{retrieved_context}")
    
    full_context = "\n\n".join(context_sections)

    # 5) 컨텍스트 크기 관리 및 품질 보장
    max_context_length = 25000  # 안전한 컨텍스트 길이
    if len(full_context) > max_context_length:
        print(f"   ⚠️ Context length ({len(full_context)}) exceeds limit, applying intelligent truncation")
        
        # 이전 Q&A는 최대한 보존하고 검색 문서를 조정
        if previous_qa_context:
            # 이전 Q&A 크기 확인
            qa_context_size = len(previous_qa_context) + 500  # 여유분
            remaining_space = max_context_length - qa_context_size
            
            if remaining_space > 1000:  # 충분한 공간이 있으면
                truncated_retrieved = retrieved_context[:remaining_space] + "\n\n[Retrieved context truncated due to length]"
                full_context = f"=== Previous Steps Q&A ===\n{previous_qa_context}\n\n=== Step {current_step} Retrieved Documents ===\n{truncated_retrieved}"
            else:
                # 공간이 부족하면 이전 Q&A도 최신 부분만 유지
                recent_qa_limit = max_context_length // 2
                truncated_qa = previous_qa_context[-recent_qa_limit:] + "\n[Previous Q&A truncated, showing recent parts only]"
                truncated_retrieved = retrieved_context[:max_context_length//2] + "\n[Retrieved context truncated]"
                full_context = f"=== Previous Steps Q&A (Recent) ===\n{truncated_qa}\n\n=== Step {current_step} Retrieved Documents ===\n{truncated_retrieved}"
        else:
            # 이전 Q&A가 없으면 검색 문서만 조정
            full_context = retrieved_context[:max_context_length] + "\n\n[Retrieved context truncated due to length]"
        
        print(f"   📏 Final context length: {len(full_context)} characters")

    # 6) 하위 질문에 대한 답변 생성 (요구사항 2: 전체 컨텍스트 활용)
    print(f"   🤖 Generating answer for Step {current_step} with full context...")
    answer = utils.generate_llm_answer(subquestion, full_context)

    print(f"   ✅ Step {current_step} completed (answer length: {len(answer)} chars)")

    return {
        "question": subquestion,
        "retrieved_context": retrieved_context,  # 현재 단계에서 검색된 문서들만
        "previous_context": previous_qa_contexts,  # 이전 단계들의 Q&A
        "full_context": full_context,  # 이전 단계 + 현재 검색 결과 (요구사항 2)
        "answer": answer,
        "explanation": explanation,
        "context_docs": context_docs,
        "step_number": current_step,  # 디버깅용 단계 번호 추가
    }


def aggregate_subquestion_results(
    original_query: str, subquestion_results: List[Dict[str, Any]]
) -> str:
    """
    하위 질문들의 결과를 종합하여 원본 질문에 대한 최종 답변을 생성합니다.

    Args:
        original_query: 원본 복잡한 질문
        subquestion_results: 하위 질문들의 처리 결과 리스트

    Returns:
        최종 종합 답변
    """
    if not subquestion_results:
        return f"Unable to process the complex question: {original_query}"

    # 모든 하위 질문의 컨텍스트와 답변을 종합
    combined_answers = ""
    all_retrieved_contexts = []

    for i, result in enumerate(subquestion_results, 1):
        combined_answers += (
            f"{i}. Q: {result['question']}\n   A: {result['answer']}\n\n"
        )

        # 각 단계에서 검색된 문서들만 수집 (중복 방지)
        if result.get("retrieved_context"):
            all_retrieved_contexts.append(
                f"=== Sub-question {i} Context ===\n{result['retrieved_context']}"
            )

    # 전체 검색된 컨텍스트
    combined_retrieved_context = "\n\n".join(all_retrieved_contexts)

    try:
        final_answer = (
            utils.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert in semiconductor physics who excels at synthesizing complex information to provide comprehensive answers.

                                    Based on sub-question answers and context, provide a comprehensive, well-structured final answer that:
                                    1. Synthesizes information from all sub-questions
                                    2. Addresses the original question directly and completely
                                    3. Is technically accurate for semiconductor physics domain
                                    4. Includes relevant details and explanations
                                    5. Shows how the sub-answers connect to form the complete solution

                                    Structure your response clearly with proper reasoning and conclusions.""",
                    },
                    {
                        "role": "user",
                        "content": f"""Original Complex Question: {original_query}

                                    Sequential sub-questions and their answers:
                                    {combined_answers}

                                    Retrieved context from all searches:
                                    {combined_retrieved_context}

                                    Please provide a comprehensive final answer to the original question.""",
                    },
                ],
                max_tokens=2000,
                temperature=0.2,
            )
            .choices[0]
            .message.content.strip()
        )

        return final_answer

    except Exception as e:
        print(f"Error in final answer generation: {e}")
        # Fallback: simple concatenation
        return f"Based on the sequential analysis of sub-questions:\n\n{combined_answers}\n\nThese findings address the original question: {original_query}"


def process_complex_query(
    original_query: str,
    retrieval_type: Optional[str] = None,
    hybrid_weights: Optional[List[float]] = None,
    max_subquestions: int = 5,
) -> Dict[str, Any]:
    """
    복잡한 질문에 대한 전체 처리 과정을 수행합니다.
    하위 질문들을 순차적으로 처리하며, 각 단계에서 이전 단계의 질문-답변을 컨텍스트로 활용합니다.

    Args:
        original_query: 원본 복잡한 질문
        retrieval_type: 검색 타입
        hybrid_weights: 하이브리드 검색 가중치
        max_subquestions: 최대 하위 질문 개수

    Returns:
        최종 결과를 포함한 딕셔너리
    """
    print(f"🔍 Processing complex query: {original_query}")

    try:
        # 1. 질문 분해 (요구사항 1)
        print("📝 Step 1: Decomposing query into sub-questions...")
        subquestions = decompose_query(original_query, max_subquestions)

        if not subquestions:
            print("⚠️ Warning: No sub-questions generated, falling back to simple processing")
            return {
                "original_query": original_query,
                "subquestions": [original_query],
                "subquestion_results": [],
                "final_answer": f"Unable to decompose query. Processing as simple query: {original_query}",
                "combined_context": "",
                "all_context_docs": [],
            }

        print(f"📋 Generated {len(subquestions)} sub-questions:")
        for i, sq in enumerate(subquestions, 1):
            print(f"  {i}. {sq}")

        # 2. 각 하위 질문을 순차적으로 처리 (요구사항 1 & 2)
        print("⚡ Step 2: Processing sub-questions sequentially with cumulative context...")
        subquestion_results = []

        for i, subquestion in enumerate(subquestions, 1):
            try:
                print(f"\n🔄 Processing Step {i}/{len(subquestions)}")
                print(f"   Question: {subquestion}")

                # 요구사항 2: 이전 단계들의 결과를 모두 전달하여 cumulative context 구성
                result = process_subquestion(
                    subquestion,
                    retrieval_type,
                    hybrid_weights,
                    previous_results=subquestion_results,  # 누적된 이전 단계들의 결과
                )

                subquestion_results.append(result)

                print(f"   ✅ Step {i} completed successfully")
                print(f"   📊 Context included: {len(result.get('previous_context', []))} previous Q&A pairs + current retrieval")

            except Exception as e:
                print(f"   ❌ Error processing Step {i}: {e}")
                # 에러가 발생한 하위 질문에 대해서도 기본 결과 추가
                error_result = {
                    "question": subquestion,
                    "retrieved_context": "",
                    "previous_context": [],
                    "full_context": "",
                    "answer": f"Error processing this sub-question: {str(e)}",
                    "explanation": "",
                    "context_docs": [],
                    "step_number": i,
                }
                subquestion_results.append(error_result)

        # 3. 결과 종합
        print("Step 3: Aggregating sequential results...")
        try:
            final_answer = aggregate_subquestion_results(
                original_query, subquestion_results
            )
        except Exception as e:
            print(f"Error in aggregation: {e}")
            # 폴백: 간단한 답변 조합
            answers = [
                result["answer"] for result in subquestion_results if result["answer"]
            ]
            final_answer = (
                f"Based on the sequential sub-questions analysis:\n\n"
                + "\n\n".join(answers)
            )

        # 모든 컨텍스트 통합
        all_retrieved_contexts = []
        all_context_docs = []

        for i, result in enumerate(subquestion_results, 1):
            if result.get("retrieved_context"):
                all_retrieved_contexts.append(
                    f"=== Step {i} Retrieved Context ===\n{result['retrieved_context']}"
                )
            if result.get("context_docs"):
                all_context_docs.extend(result["context_docs"])

        combined_context = "\n\n".join(all_retrieved_contexts)

        # 누적 Q&A 컨텍스트 구성 (디버깅 및 추적용)
        cumulative_qa_parts = []
        for i, result in enumerate(subquestion_results, 1):
            cumulative_qa_parts.append(f"Step {i} Q: {result['question']}\nStep {i} A: {result['answer']}")
        cumulative_qa_context = "\n\n".join(cumulative_qa_parts)

        print("✅ Sequential complex query processing completed successfully")
        print(f"📈 Total steps processed: {len(subquestion_results)}")

        return {
            "original_query": original_query,
            "subquestions": subquestions,
            "subquestion_results": subquestion_results,
            "final_answer": final_answer,
            "combined_context": combined_context,
            "all_context_docs": all_context_docs,
            "cumulative_qa_context": cumulative_qa_context,  # 전체 Q&A 진행 과정
            "processing_summary": f"Processed {len(subquestions)} sub-questions with cumulative context",
        }

    except Exception as e:
        print(f"💥 Critical error in complex query processing: {e}")
        # 최종 폴백
        return {
            "original_query": original_query,
            "subquestions": [original_query],
            "subquestion_results": [],
            "final_answer": f"Error processing complex query: {str(e)}. Please try rephrasing your question.",
            "combined_context": "",
            "all_context_docs": [],
            "cumulative_qa_context": "",
            "processing_summary": "Error occurred during processing",
        }


def process_complex_query_with_expansion(
    original_query: str,
    content_docs: List[Document],
    example_docs: List[Dict[str, Any]],
    retrieval_type: Optional[str] = None,
    hybrid_weights: Optional[List[float]] = None,
    max_subquestions: int = 5,
) -> Dict[str, Any]:
    """
    사전 검색된 content와 examples를 활용하여 복잡한 질문을 처리합니다.
    Query expansion을 통해 얻은 컨텍스트를 초기 정보로 활용하며,
    하위 질문들을 순차적으로 처리하면서 이전 단계의 질문-답변을 누적합니다.

    Args:
        original_query: 원본 복잡한 질문
        content_docs: 사전 검색된 content 문서들
        example_docs: 사전 검색된 example 문서들
        retrieval_type: 검색 타입
        hybrid_weights: 하이브리드 검색 가중치
        max_subquestions: 최대 하위 질문 개수

    Returns:
        최종 결과를 포함한 딕셔너리
    """
    print(f"🔍 Processing complex query with expansion: {original_query}")
    print(f"📊 Initial resources: {len(content_docs)} content docs, {len(example_docs)} example docs")

    try:
        # 1. 초기 컨텍스트 구성 (사전 검색된 데이터 활용)
        print("📝 Step 1: Building initial context from pre-retrieved data...")
        initial_context_parts = []

        if content_docs:
            content_texts = []
            for doc in content_docs:
                if hasattr(doc, "page_content"):
                    content_texts.append(doc.page_content)
                else:
                    content_texts.append(str(doc))
            
            if content_texts:
                initial_context_parts.append(
                    "Available Content:\n" + "\n".join(content_texts[:3])
                )  # Limit for context size

        if example_docs:
            example_texts = []
            for doc in example_docs:
                if isinstance(doc, dict):
                    example_texts.append(doc.get("page_content", str(doc)))
                else:
                    example_texts.append(str(doc))
            
            if example_texts:
                initial_context_parts.append(
                    "Available Examples:\n" + "\n".join(example_texts[:2])
                )  # Limit for context size

        initial_context = "\n\n".join(initial_context_parts)
        print(f"   📏 Initial context length: {len(initial_context)} characters")

        # 2. 컨텍스트 인식 질문 분해
        print("🔧 Step 2: Decomposing query with context awareness...")

        try:
            response = utils.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are an expert in semiconductor physics who excels at breaking down complex questions into simpler, manageable sub-questions.

Given a complex question and available context (content documents and examples), break it down into {max_subquestions} or fewer sub-questions that:
1. Are simpler and more focused than the original question
2. Build upon each other logically 
3. Leverage the available context and examples effectively
4. When answered together, provide comprehensive information to solve the original question
5. Are specific to semiconductor physics domain

The available context includes:
- Technical content documents with theoretical background
- Example documents with practical applications and calculations

Format your response as a numbered list:
1. [First sub-question]
2. [Second sub-question]
...

Respond with ONLY the numbered list of sub-questions.""",
                    },
                    {
                        "role": "user",
                        "content": f"""Complex Question: {original_query}

Available Context:
{initial_context}

Break down this question into focused sub-questions that can effectively leverage the available context.""",
                    },
                ],
                max_tokens=1000,
                temperature=0.3,
            )

            response_text = response.choices[0].message.content.strip()
            subquestions = []
            lines = response_text.split("\n")

            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith("-")):
                    if ". " in line:
                        question = line.split(". ", 1)[1].strip()
                    elif "- " in line:
                        question = line.split("- ", 1)[1].strip()
                    else:
                        question = line.strip()

                    if question and len(question) > 10:
                        subquestions.append(question)

            if not subquestions:
                print("   ⚠️ Warning: No context-aware sub-questions generated, using fallback")
                subquestions = [
                    f"What are the fundamental concepts related to: {original_query}?",
                    f"How can the available examples help understand: {original_query}?",
                    f"What are the key factors that influence: {original_query}?",
                ]

            subquestions = subquestions[:max_subquestions]
            print(f"   ✅ Generated {len(subquestions)} context-aware sub-questions")

        except Exception as e:
            print(f"   ❌ Error in context-aware query decomposition: {e}")
            print("   🔄 Falling back to standard decomposition...")
            subquestions = decompose_query(original_query, max_subquestions)

        if not subquestions:
            print("   ❌ Critical: No sub-questions could be generated")
            return {
                "original_query": original_query,
                "subquestions": [original_query],
                "subquestion_results": [],
                "final_answer": f"Unable to decompose query with expansion: {original_query}",
                "combined_context": initial_context,
                "all_context_docs": content_docs,
                "cumulative_qa_context": "",
                "processing_summary": "Failed to decompose query",
            }

        print(f"📋 Final sub-questions for processing:")
        for i, sq in enumerate(subquestions, 1):
            print(f"  {i}. {sq}")

        # 3. 순차적 하위 질문 처리 (초기 컨텍스트 포함)
        print("⚡ Step 3: Processing sub-questions sequentially with initial context...")
        subquestion_results = []
        
        # 초기 컨텍스트를 첫 번째 단계의 "이전 결과"로 활용
        initial_result = {
            "question": "Initial Context (Pre-retrieved Content & Examples)",
            "answer": initial_context,
        } if initial_context else None

        for i, subquestion in enumerate(subquestions, 1):
            try:
                print(f"Processing sub-question {i}/{len(subquestions)}: {subquestion}")

                # 이전 결과들 + 초기 컨텍스트 포함
                previous_results_with_context = []
                if initial_result and i == 1:
                    # 첫 번째 단계에서만 초기 컨텍스트 포함
                    previous_results_with_context.append(initial_result)
                    print(f"   📚 Including initial context for first step")
                
                # 모든 이전 단계의 결과 누적
                previous_results_with_context.extend(subquestion_results)
                
                print(f"   📊 Total context sources: {len(previous_results_with_context)}")

                # 하위 질문 처리 (요구사항 2: 누적 컨텍스트 사용)
                result = process_subquestion(
                    subquestion,
                    retrieval_type,
                    hybrid_weights,
                    previous_results=previous_results_with_context,
                )

                subquestion_results.append(result)

                print(f"   ✅ Step {i} completed successfully")
                # print(f"   📈 Answer length: {len(result.get('answer', ''))} characters")

            except Exception as e:
                print(f"   ❌ Error processing Step {i}: {e}")
                # 에러 발생 시에도 기본 결과 추가
                error_result = {
                    "question": subquestion,
                    "retrieved_context": "",
                    "previous_context": [],
                    "full_context": "",
                    "answer": f"Error processing this sub-question: {str(e)}",
                    "explanation": "",
                    "context_docs": [],
                    "step_number": i,
                }
                subquestion_results.append(error_result)

        # 4. 최종 답변 종합
        print("🎯 Step 4: Aggregating sequential results into final answer...")
        try:
            final_answer = aggregate_subquestion_results(
                original_query, subquestion_results
            )
            print(f"   ✅ Final answer generated (length: {len(final_answer)} characters)")
        except Exception as e:
            print(f"   ❌ Error in final aggregation: {e}")
            print("   🔄 Using fallback aggregation...")
            # 폴백: 간단한 답변 조합
            answers = [
                result["answer"] for result in subquestion_results if result.get("answer")
            ]
            final_answer = (
                f"Based on sequential analysis with expansion:\n\n"
                + "\n\n".join(answers)
            )

        # 5. 모든 컨텍스트 통합
        print("📚 Step 5: Consolidating all contexts...")
        all_retrieved_contexts = []
        all_context_docs = list(content_docs)  # 초기 content 문서들로 시작

        # 초기 컨텍스트 추가
        if initial_context:
            all_retrieved_contexts.append(f"=== Initial Context ===\n{initial_context}")

        # 각 단계에서 검색된 컨텍스트 추가
        for i, result in enumerate(subquestion_results, 1):
            if result.get("retrieved_context"):
                all_retrieved_contexts.append(
                    f"=== Step {i} Retrieved Context ===\n{result['retrieved_context']}"
                )
            if result.get("context_docs"):
                all_context_docs.extend(result["context_docs"])

        combined_context = "\n\n".join(all_retrieved_contexts)

        # 6. 누적 Q&A 컨텍스트 구성 (전체 진행 과정 추적용)
        print("📝 Step 6: Building cumulative Q&A context...")
        cumulative_qa_parts = []
        
        if initial_context:
            cumulative_qa_parts.append(f"Initial Context:\n{initial_context}")
        for i, result in enumerate(subquestion_results, 1):
            cumulative_qa_parts.append(
                f"Step {i} Q: {result['question']}\n"
                f"Step {i} A: {result['answer']}"
            )
        
        cumulative_qa_context = "\n\n".join(cumulative_qa_parts)

        print("✅ Complex query processing with expansion completed successfully")
        print(f"📈 Processing summary:")
        print(f"   - Original query: {original_query}")
        print(f"   - Sub-questions processed: {len(subquestion_results)}")
        print(f"   - Total context docs: {len(all_context_docs)}")
        print(f"   - Final answer length: {len(final_answer)} characters")

        return {
            "original_query": original_query,
            "subquestions": subquestions,
            "subquestion_results": subquestion_results,
            "final_answer": final_answer,
            "combined_context": combined_context,
            "all_context_docs": all_context_docs,
            "cumulative_qa_context": cumulative_qa_context,
            "processing_summary": f"Processed {len(subquestions)} sub-questions with expansion context (content: {len(content_docs)}, examples: {len(example_docs)})",
        }

    except Exception as e:
        print(f"💥 Critical error in complex query processing with expansion: {e}")
        import traceback
        traceback.print_exc()
        
        # 최종 폴백
        return {
            "original_query": original_query,
            "subquestions": [original_query],
            "subquestion_results": [],
            "final_answer": f"Error processing complex query with expansion: {str(e)}. Please try rephrasing your question.",
            "combined_context": "",
            "all_context_docs": content_docs,
            "cumulative_qa_context": "",
            "processing_summary": f"Error occurred during expansion processing: {str(e)}",
        }
