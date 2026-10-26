# Answer Generation

The Helix Engineering Platform uses a retrieval-augmented generation pipeline to produce answers grounded in the indexed engineering knowledge base.

## Generation Pipeline

After retrieval completes, the answer generation layer performs the following steps:

1. Receive the user's query
2. Select the highest-ranked retrieved chunks
3. Build the context provided to the language model
4. Generate an answer using the retrieved evidence
5. Associate claims with supporting source chunks
6. Return the answer and citations

The language model is used for reasoning over retrieved information rather than as the primary source of engineering knowledge.

## Retrieved Context

Only relevant retrieved chunks are included in the generation context.

Each context item contains the chunk content together with source metadata such as document identifier, title, section, and chunk identifier.

The generation layer uses this metadata to preserve the relationship between an answer and its supporting evidence.

## Grounded Answers

The model should answer questions using the retrieved context.

If the retrieved documents contain sufficient evidence, the response should provide a concise answer supported by citations.

If the retrieved context does not contain enough information to answer a question reliably, the system should state that the available knowledge base does not contain sufficient information.

The system should not invent configuration values, architecture details, or operational behavior that is not supported by the retrieved evidence.

## Citations

Generated claims are associated with the source chunks that support them.

A citation identifies the document and chunk used as evidence.

For example, an answer about API rate limiting may cite the API Gateway document, while an answer about Kafka consumer lag may cite the Observability document.

Citations make generated answers auditable and allow users to inspect the underlying engineering documentation.

## Context Limits

The generation layer limits the amount of retrieved context provided to the language model.

Sending excessive unrelated content can reduce answer quality and increase generation cost.

The retrieval layer therefore provides a ranked top-k set of relevant chunks rather than the entire document collection.

## Answer Quality

Answer quality depends on both retrieval quality and generation quality.

A correct language model cannot produce a reliable grounded answer when the required evidence was not retrieved.

Similarly, strong retrieval does not guarantee a good answer if the model ignores relevant context or introduces unsupported claims.

The system therefore evaluates retrieval, citations, and generated answers independently.

## Failure Handling

If retrieval fails, answer generation does not attempt to fabricate an answer.

If the language model is unavailable, the application returns an explicit generation error.

If retrieved context is insufficient, the system reports that the knowledge base does not contain enough information rather than presenting an unsupported response.

## Streaming

The API can stream generated answer tokens to the client.

Streaming allows users to see the response progressively instead of waiting for the entire generation to finish.

Citations are returned as part of the final response metadata so that the complete answer remains associated with its supporting sources.

## Security

User queries and retrieved documents are treated as application data.

Secrets, access tokens, credentials, and other sensitive configuration values must not be inserted into prompts unless explicitly required by an authorized operation.

The generation layer must also avoid exposing information that the requesting user is not authorized to access.
