
from typing import Any, Dict, List, Optional


from team_builder.nodes.interface import Iinputs

from .enums import NodeType
from .node import Node

from langchain_community.vectorstores import Pinecone
from langchain.retrievers import ContextualCompressionRetriever
from langchain.schema import format_document
from langchain.prompts.prompt import PromptTemplate
from langchain_core.documents import Document
from langchain_cohere import CohereRerank
import os





class RetriverNode(Node):
    question:str
    index:str
    namespace:str
    embedding: Any
    k:Optional[int]
    n:Optional[int]
    rerank_score: Optional[float]
    filter: List[Dict]
    loaders: List[Dict]



    @property
    def type(self):
        return NodeType.RETRIVER
    
    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls(
            id = kwargs["id"],
            name = kwargs["name"],
            description = kwargs.get("description"),
            question = kwargs["question"],
            index = "basic",
            namespace = os.environ['NAMESPACE'],
            k = kwargs.get("k", 10),
            n = kwargs.get("n", 4),
            rerank_score = kwargs.get("rerank_score"),
            embedding = "embedding",
            filter = kwargs.get("filter", []),
            loaders = kwargs.get("loaders", [])

        )


    def execute(self, inputs:Iinputs) -> str | Dict | List :
        docs = self._rernk(self.get_relevant_documents(self.convert_varibales(self.question, inputs)))
        metadata = []
        for x in docs:
            metadata.append({"content":x.page_content, "metadata": x.metadata})
        format_docs = self.format_docs(docs)
        string_docs = self.get_doc_string(format_docs)
        return {"context": string_docs, "documents": metadata}
        #return self.get_doc_string(docs)

    # @property
    # def Embeddings(self):
    #     match self.embeding_model:
    #         case EmbeddingModel.TITAN_1:
    #             if not self.aws_config:
    #                 aws_config = {"region_name":'us-east-1'}
    #             bedrock = boto3.client(service_name='bedrock-runtime', **aws_config)
    #             return BedrockEmbeddings(client=bedrock, model_id=self.embeding_model)
    #         case EmbeddingModel.OPEN_AI_SMALL:
    #             return OpenAIEmbeddings(model=self.embeding_model)
    #         case _:
    #             if self.azure_config:
    #                 return AzureOpenAIEmbeddings(**self.azure_config)
    #             return OpenAIEmbeddings()


    
    def get_relevant_documents(self, query:str) -> List[Document]:
        _list = []
        loader_urls = []
        for loader in self.loaders:
            if loader['type'] == 'URL':
                for url in loader['urls']:
                    loader_urls.append(url['url'])
            else:
                loader_urls.append(loader['id'])

        # for x in self.filter:
        #     if x['id'] in loader_urls:
        #         if x['type'] == LoaderType.URL:
        #             _list.append(x['id'])
        #         else:
        #             _list.append(f"{self.namespace}/{x['id']}")

        filter = {'source':{ "$in": _list }} if _list else {}
        vectorstore = Pinecone.from_existing_index(self.index, self.embedding, namespace=self.namespace)
        retriever = vectorstore.as_retriever(search_kwargs={"k":self.k, "filter":filter})
        compressor = CohereRerank(model="rerank-multilingual-v2.0", top_n=self.n)
        return ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever).invoke(query)
    

    
    def _rernk(self, docs:List[Document]) -> List[Document]:
        if not self.rerank_score:
            return docs
        return [doc for doc in docs if doc.metadata["relevance_score"] >= self.rerank_score]
    
    def format_docs(self, docs:List[Document]) -> List[Dict]:
        document_prompt = PromptTemplate.from_template(template="{page_content}")
        return [format_document(doc, document_prompt) for doc in docs] #type: ignore
    
    def get_doc_string(self, docs, document_separator="\n\n"):
        return document_separator.join(docs)

    
        


        
            















        


