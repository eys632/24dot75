from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_teddynote.messages import stream_response
from langchain_core.output_parsers import JsonOutputParser

from datetime import datetime
from pydantic import BaseModel, Field

from database_process import select_docs

def answer_output_parser():
    class QuestionSummary(BaseModel):
        summary: str = Field(description="Text that briefly summarizes the question")

    class AnswerDetails(BaseModel):
        main_content: list = Field(description="A collection of texts for searched and cited information")
        metadata: list = Field(description="All metadata about the information you found and cited(chunk_id, page_number, chunk_length)")

    class Conclusion(BaseModel):
        conclusion: str = Field(description="A comprehensive summary based on the documentation. Organized in great detail and detail. Don't try to summarize. Rather, use the documentation to expand on")

    class QuestionResponse(BaseModel):
        question_summary: QuestionSummary = Field(description="Question summary information In markdown format")
        answer: AnswerDetails = Field(description="The answer to the question and the metadata")
        conclusion: Conclusion = Field(description="A very detailed conclusion to the question In markdown format")

    parser = JsonOutputParser(pydantic_object=QuestionResponse)

    return parser

def question_output_parser():
    class QuestionEvaluation(BaseModel):
        next: bool = Field(
            description=(
                """An assessment of whether the answer is complete and appropriate. True means the answer is complete and does not require revision,
                False indicates that the answer is incomplete or needs improvement."""
            )
        )
        scroe: float = Field(
            description=(
                """The score (value between 0.0 and 1.0) of the LLM-generated answer."""
            )
        )
        new_query: str = Field(
            description=(
                """Newly generated question to help LLM provide a more accurate and appropriate answer. Provide a query to help MMR find it better. Returns null if the answer is perfect."""
            ),
            default=None,
        )
        reason: str = Field(
            description=(
                """Reasons for your assessment results. If the answer is perfect, why,
                If incomplete, explain what needs to be improved and the need to create a new question."""
            )
        )

    parser = JsonOutputParser(pydantic_object=QuestionEvaluation)

    return parser

def define_prompts(answer_parser, question_parser):

  answer_prompt = ChatPromptTemplate.from_messages([
    ("system", f"""
            [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]
            # Query and Documentation Analysis Guidelines

            ## Step 1: Query and Document Analysis
            1. **Query Breakdown**:  
              - If the query is complex, break it into smaller, more manageable parts.  
              - Focus exclusively on the content provided in the document.  
              - Avoid including any information not explicitly mentioned in the document.

            ## Step 2: Writing a Detailed Answer
            1. **Use Clear Language**:  
              - Write in a simple and easy-to-understand way that even a middle school student can follow.  
            2. **Organize Logically**:  
              - Make sure your explanation flows well and has a clear structure.  
            3. **Be Thorough**:  
              - Cover all relevant points and provide detailed explanations.  

            ## Step 3: Formatting Requirements
            1. Use **Markdown format** within a JSON structure for clear presentation.  
            2. Utilize:  
              - **Headings** for different sections.  
              - **Bullet points** or **numbered lists** for clarity and readability.  

            ## Step 4: Language and Style
            1. Write entirely in **Korean**.  
            2. Avoid using technical jargon.  
            3. Explain concepts in a way that is engaging and relatable for readers.
            """),
    ("human", """
                # Format : {format_instructions}
                # query : {instruction}
                # docs : {mmr_docs}
            """),
    ])

  question_prompt = ChatPromptTemplate.from_messages([
  ("system", f"""[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]
  You are tasked with evaluating the quality of an answer provided by an LLM based on a given question and relevant documentation. Follow these steps to ensure the evaluation is accurate, consistent, and complete:

  1. **Evaluate the answer for completeness and appropriateness**:
    - **If the answer is complete**:
      - Return `True` if the documentation perfectly matches the question, and the LLM-generated answer is accurate and complete without requiring further editing.
      - Provide a reason explaining why the answer is considered complete.

    - **If the answer is incomplete**:
      - Return `False` if the answer does not fully address the question, lacks relevance to the documentation, or can be improved.
      - Provide a detailed reason explaining the shortcomings of the answer.
      - Rewrite the question to help the LLM generate a more accurate and relevant answer. The new question should:
        - Be specific and clear.
        - Focus solely on the content of the document.
        - Remove redundant or irrelevant details.
        - Add any additional context or details necessary to clarify the query.

  2. **Scoring the answer**:
    - Provide a score between `0.0` and `1.0` to represent how well the answer meets the question's requirements and aligns with the documentation:
      - `1.0`: Perfectly aligned and requires no changes.
      - `0.0`: Completely misaligned or irrelevant.

  3. **Answer requirements**:
    - Write both new questions and explanations in simple, clear Korean that a middle school student can easily understand.
    - Avoid technical jargon and explain concepts in a friendly and engaging tone.
    - Ensure the response is logical, well-structured, and sufficiently detailed to avoid ambiguity.

  4. **Formatting requirements**:
    - Provide the evaluation results in the following JSON format:
    ```json
        "next": true or false,
        "score": 0.0 to 1.0,
        "new_query": "Newly rewritten question if necessary, or null if the answer is perfect.",
        "reason": "Explanation of why the answer is complete or what improvements are needed."
    ```

  5. **Key Input Variables**:
    - `original_question`: The original query posed to the LLM.
    - `llm_answer`: The answer provided by the LLM.
    - `document_context`: The relevant documentation used to generate the answer.

  Use the input variables effectively to analyze and generate your evaluation and output. Your goal is to provide an insightful assessment and actionable feedback in JSON format.
    """),
  ("human", """instruction : {instruction},
                docs : {mmr_docs},
                llm_answer : {llm_answer}"""),
  ])

  # Partial Prompts with Formatting Instructions
  answer_prompt = answer_prompt.partial(format_instructions=answer_parser.get_format_instructions())
  question_prompt = question_prompt.partial(format_instructions=question_parser.get_format_instructions())

  return answer_prompt, question_prompt

  # 체인 생성 함수
def create_chains(llm, answer_prompt, question_prompt, answer_parser, question_parser):
  answer_chain = answer_prompt | llm | answer_parser
  question_chain = question_prompt | llm | question_parser
  return answer_chain, question_chain

# 쿼리 실행 및 결과 반환 함수
def execute_chains(answer_chain, question_chain, query, mmr_docs):
  # Answer Chain Execution
  answer_q = {"instruction": query, "mmr_docs": mmr_docs}
  answer = answer_chain.invoke(answer_q)

  # Question Chain Execution
  question_q = {"instruction": query, "mmr_docs": mmr_docs, "llm_answer": answer}
  question = question_chain.invoke(question_q)

  return answer, question

# Main 함수
def generate_response(db, query):
  
  answer_parser = answer_output_parser()
  question_parser = question_output_parser()

  # Define Prompts
  answer_prompt, question_prompt = define_prompts(answer_parser, question_parser)

  # Initialize LLM
  llm = ChatOpenAI(temperature=0, model_name="gpt-4o")

  # Create Chains
  answer_chain, question_chain = create_chains(llm, answer_prompt, question_prompt, answer_parser, question_parser)

  for i in range(10):
    mmr_docs = select_docs(db, query)

    # Execute Chains and Get Results
    answer, question = execute_chains(answer_chain, question_chain, query, mmr_docs)
    
    if question["next"]:
      break
    else:
      continue

  return answer, question