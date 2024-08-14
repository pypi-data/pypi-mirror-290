from nebuia_copilot_python.src.extractor.extractor import Extractor
from typing import Dict, List

from loguru import logger

from nebuia_copilot_python.src.listener.listener_integrator import ListenerIntegrator
from nebuia_copilot_python.src.api_client import APIClient
from nebuia_copilot_python.src.models import BatchDocumentsResponse, BatchType, Document, DocumentType, EntityDocumentExtractor, EntityTextExtractor, File, Job, ResultsSearch, Search, SearchDocument, SearchParameters, StatusDocument, UploadResult


class Integrator:

    def __init__(self, with_base: str, key: str, secret: str) -> None:
        """
        Initializes a new instance of the class with the provided API credentials.

        This constructor sets up the API client with the given base URL, API key,
        and API secret. These credentials are necessary for authenticating and
        interacting with the API.

        Args:
            with_base (str): The base URL of the API.
            key (str): The API key for authentication.
            secret (str): The API secret for authentication.

        Returns:
            None
        """
        self._api_client = APIClient(
            key=key,
            secret=secret,
            base=with_base
        )

        self.listener = self._create_listener_integrator(self._api_client)
        self._extractor = Extractor(self._api_client)

    def _create_listener_integrator(self, api_client: APIClient) -> ListenerIntegrator:
        """
        create instance from ListenerIntegrator.
        """
        return ListenerIntegrator(api_client)

    def create_batch(self, name_batch: str, batch_type: BatchType):
        """
        Creates a new batch using the provided name and type, and returns the result.

        This method communicates with an external API to create a batch. It logs the generated batch ID upon success
        and returns a tuple indicating the success status and either the batch ID or error details.

        Args:
            name_batch (str): The name of the batch to be created.
            batch_type (BatchType): The type of the batch, which should be an instance of the `BatchType` enum or a similar type.

        Returns:
            tuple: A tuple containing:
                - success (bool): True if the batch was created successfully, False otherwise.
                - result (str or dict): If successful, the `batch ID (str)`. If unsuccessful, the payload from the response,
                typically containing error information (dict).

        Example:
            >>> success, result = create_batch("My Batch", BatchType.SOME_TYPE)
            >>> if success:
            ...     print(f"Batch created successfully with ID: {result}")
            ... else:
            ...     print(f"Failed to create batch: {result}")

        Raises:
            None: This method does not raise any exceptions. Instead, it returns error details in the response.

        Notes:
            - Ensure that the `BatchType` enum or type is correctly defined and used in your application.
            - The API client should be properly initialized and configured to make successful API calls.
        """
        response = self._api_client.create_batch(
            name_batch, batch_type)
        if response.status:
            batch_id = response.payload
            logger.info(f"generated batch id: {batch_id}")
            return True, batch_id
        else:
            return False, response.payload

    def append_to_batch(self, batch_id: str, files: list[File]) -> Dict[str, List[UploadResult]]:
        """
        Appends a list of files to a specified batch and returns the results of the upload operation.

        Args:
            batch_id (str): The identifier of the batch to which the files should be appended.
            files (List[File]): A list of File objects to be appended to the batch.

        Returns:
            Dict[str, List[UploadResult]]: A dictionary containing the results of the upload operation.
                - "successful": A list of UploadResult objects for successful uploads.
                - "failed": A list of UploadResult objects for failed uploads.

        Raises:
            None
        """
        job = Job(files=files)
        response = self._api_client.append_job(job, batch_id)
        return response

    def get_document_types(self) -> List[DocumentType]:
        """
        Retrieve all document types available for the current user.

        This method fetches the list of document types from the API using the
        configured API client. Each document type contains information such as
        its ID, user, key, type document ID, and creation date.

        Returns:
            List[DocumentType]: A list of DocumentType objects representing the 
            different document types available for the user.

        Raises:
            APIError: If there's an error communicating with the API.
            AuthenticationError: If the user's authentication is invalid or expired.
            ParseError: If the response from the API cannot be parsed correctly.

        Example:
            >>> document_types = integrator.get_document_types()
            >>> for doc_type in document_types:
            ...     print(f"{doc_type.key}: {doc_type.id_type_document}")

        Note:
            This method relies on the `_api_client.get_document_types()` method to
            perform the actual API request. Ensure that the API client is properly
            configured before calling this method.

        See Also:
            DocumentType: For the structure of each document type object.
            APIClient.get_document_types: For details on the underlying API call.
        """
        return self._api_client.get_document_types()

    def get_documents_by_batch_id(self, batch_id: str) -> BatchDocumentsResponse:
        """
        Retrieve documents associated with a specific batch ID.

        This method fetches all documents linked to the provided batch ID using
        the configured API client. It returns a structured representation of the
        documents and their details, including any associated entities.

        Args:
            batch_id (str): The unique identifier of the batch for which to retrieve documents.

        Returns:
            BatchDocumentsResponse: An object containing:
                - documents (List[Document]): A list of Document objects, each representing
                  a document in the batch with its associated details and entities.
                - total (int): The total number of documents in the batch.

        Raises:
            APIError: If there's an error communicating with the API.
            AuthenticationError: If the user's authentication is invalid or expired.
            ValueError: If the batch_id is invalid or not found.
            ParseError: If the response from the API cannot be parsed correctly.

        Example:
            >>> batch_response = integrator.get_documents_by_batch_id("66a5271a7a97c83cece5dd0d")
            >>> print(f"Total documents in batch: {batch_response.total}")
            >>> for doc in batch_response.documents:
            ...     print(f"Document: {doc.file_name}, Status: {doc.status_document}")
            ...     if doc.entities:
            ...         for entity in doc.entities:
            ...             print(f"  Entity: {entity.key} = {entity.value}")

        Note:
            - The 'entities' field in each document is optional and will be included
              only if present in the API response.
            - This method relies on the `_api_client.get_documents_by_batch()` method
              to perform the actual API request. Ensure that the API client is properly
              configured before calling this method.

        See Also:
            BatchDocumentsResponse: For the structure of the returned object.
            Document: For the structure of each document object.
            Entity: For the structure of each entity object within a document.
        """
        return self._api_client.get_documents_by_batch(batch_id)

    def delete_document(self, uuid: str) -> bool:
        """
        Deletes a document from a batch using its unique identifier (UUID).

        This method constructs a URL based on the provided UUID and sends a DELETE request
        to remove the specified document from the batch. The response from the server is
        then parsed as JSON and returned.

        Args:
            uuid (str): The unique identifier of the document to be deleted.

        Returns:
            bool: bool containing information about the success or failure of the deletion operation.

        Raises:
            requests.exceptions.RequestException: If there is an issue with the network
                                                or the server response.

        Example:
            >>> result = integrator.delete_document_from_batch("some-unique-identifier")
            >>> print(result)
            True
        """
        return self._api_client.delete_document_from_batch(uuid=uuid)

    def clear_document_by_uuid(self, uuid: str) -> bool:
        """
        Clears a document from the system using its unique identifier (UUID).

        This method constructs a URL based on the provided UUID and sends a GET request
        to clear the specified document from the system. The response from the server is
        then parsed as JSON, and the method returns the status of the operation.

        Args:
            uuid (str): The unique identifier of the document to be cleared.

        Returns:
            bool: True if the document was cleared successfully, False otherwise.

        Raises:
            requests.exceptions.RequestException: If there is an issue with the network
                                                or the server response.

        Example:
            >>> result = integrator.clear_document_by_uuid("some-unique-identifier")
            >>> print(result)
            True
        """
        return self._api_client.clear_document_by_uuid(uuid=uuid)

    def get_documents_by_status_and_batch(self, status: StatusDocument, batchType: BatchType, page: int = 1, limit: int = 10) -> BatchDocumentsResponse:
        return self._api_client.get_documents_by_status_and_batch(status=status, batch_type=batchType, page=page, limit=limit)

    def get_documents_by_status(self, status: StatusDocument, page: int = 1, limit: int = 10) -> BatchDocumentsResponse:
        """
        Retrieves a batch of documents based on their status.

        This method delegates the task of fetching documents to the `_api_client`'s
        `get_documents_by_status` method, passing along the provided status, page,
        and limit parameters.

        Args:
            status (StatusDocument): The status of the documents to fetch. This should be an
                enum value representing the document status.
            page (int, optional): The page number of the results to fetch. Defaults to 1.
            limit (int, optional): The number of documents to fetch per page. Defaults to 10.

        Returns:
            BatchDocumentsResponse: An object containing a list of Document objects and the
                total count of documents matching the query.

        Raises:
            APIException: If there is an error while communicating with the API.
        """
        return self._api_client.get_documents_by_status(status=status, page=page, limit=limit)

    def delete_batch(self, batch_id) -> bool:
        """
        Deletes a batch with the specified batch ID using the API client.

        This method delegates the task of deleting a batch to the API client,
        which handles the actual communication with the server. It returns a
        boolean indicating whether the deletion was successful.

        Args:
            batch_id: The unique identifier of the batch to be deleted.

        Returns:
            bool: True if the batch was successfully deleted, False otherwise.
        """
        return self._api_client.delete_batch(batch_id)

    def search_in_brain(self, search_params: SearchParameters) -> ResultsSearch:
        """
        Executes a search operation using the provided search parameters.

        This method delegates the search operation to the API client, which handles
        the communication with the underlying search engine or service. It returns
        the results of the search operation encapsulated in a ResultsSearch object.

        Args:
            search_params (SearchParameters): An instance of SearchParameters containing
                the parameters for the search operation, such as the query, filters,
                and pagination settings.

        Returns:
            ResultsSearch: An instance of ResultsSearch containing the results of the
                search operation, including a list of relevant items or documents.

        Raises:
            APIException: If there is an error during the search operation, such as
                network issues, invalid parameters, or service unavailability.
        """
        return self._api_client.search_in_brain(search_params=search_params)

    def process_document_in_batch(self, batch_id: str):
        """
        Processes an item within a specified batch.

        This method sends a POST request to the integrator API to run quality
        assurance (QA) on all items within a given batch. It logs the response if
        the request is successful, or logs an error message if the request fails.

        Args:
            batch_id (str): The identifier of the batch to process.

        Returns:
            bool

        Raises:
            HTTPError: If the POST request returns an unsuccessful status code.
            JSONDecodeError: If the response content cannot be decoded as JSON.
        """
        return self._api_client.process_item(batch_id=batch_id)

    def add_listener(self, status: StatusDocument, batchType: BatchType,  interval: int, limit_documents: int):
        """
        Add a new listener to the listener manager.

        This method creates and starts a new Listener instance through the ListenerManager.
        The new listener will periodically fetch documents with the specified status.

        Args:
            status (StatusDocument): The status of documents to be fetched by the new listener.
            batchType (BatchType): The type of batches to get
            interval (int): The time interval (in seconds) between each fetch operation.
            limit_documents (int): The maximum number of documents to fetch in each operation.

        Returns:
            Listener: The newly created and started Listener instance.

        Note:
            This method delegates the creation and management of the listener to the
            ListenerManager instance. The returned Listener is already started and
            added to the list of managed listeners.

        Example:
            >>> # Creating a new listener
            >>> listener = integrator.add_listener(StatusDocument.WAITING_QA, BatchType.EXECUTION,  4, limit_documents=20)
            >>> 
            >>> # Using the listener to process documents
            >>> try:
            ...     for documents in listener.results():
            ...         data = documents.documents
            ...         for document in data:
            ...             print("Received documents:", document.file_name)
            ... except KeyboardInterrupt:
            ...     listener.stop()
            ...     print("Stopped listener.")
            Received documents: document1.pdf
            Received documents: document2.pdf
            Stopped listener.

        This example demonstrates creating a listener for documents with WAITING_QA status,
        checking every 4 seconds, and limiting to 20 documents per fetch. It then processes
        the results in a loop, printing the file names of received documents. The loop can
        be interrupted with a KeyboardInterrupt, which will stop the listener.
        """
        return self.listener.add_listener(status=status, batch_type=batchType, interval=interval, limit_documents=limit_documents)

    def set_document_status(self, uuid: str, status: StatusDocument) -> bool:
        """
        Set the status of a document identified by its UUID.

        This method delegates the task of setting the document status to the API client,
        passing the document's UUID and the new status as arguments.

        Args:
            uuid (str): The UUID of the document whose status is to be updated.
            status (StatusDocument): The new status to be set for the document.

        Returns:
            bool: True if the status was successfully updated, False otherwise.

        Raises:
            APIException: If there is an issue with the API client.

        Example:
            >>> set_document_status('123e4567-e89b-12d3-a456-426614174000', StatusDocument.APPROVED)
            True
        """
        return self._api_client.set_document_status(uuid=uuid, status=status)

    def extract_entities_from_text(self, extractor: EntityTextExtractor):
        """
        Extracts specified entities from the given text using the provided EntityTextExtractor.

        This method utilizes the underlying Extractor to process the text and extract entities
        based on the schema provided in the EntityTextExtractor.

        Args:
            extractor (EntityTextExtractor): A dataclass object containing:
                - text (str): The text from which to extract entities.
                - schema (Union[str, dict]): The schema defining the entities to extract.
                This should always be provided as a dict, specifying the entities and 
                their extraction rules.

        Returns:
            dict: A dictionary containing the extracted entities. The structure of this
                dictionary corresponds to the schema provided and includes the extracted
                entity values from the text.

        Raises:
            TypeError: If the schema is not provided as a dict.
            ValueError: If the text is empty or the schema is invalid.
            Any exceptions that might be raised by the underlying Extractor's
            extract_from_text method or the API client.

        Note:
            - The schema in the EntityTextExtractor should always be a dict. If a string
            is provided, it should be converted to a dict before calling this method.
            - This method does not modify the input extractor object. Any necessary
            preprocessing is handled by the underlying Extractor class.

        Example:
            extractor = EntityTextExtractor(
                text="John Doe is 30 years old and lives in New York.",
                schema={
                    "name": "",
                    "age": "",
                    "location": ""
                }
            )
            entities = obj.extract_entities_from_text(extractor)
        """
        return self._extractor.extract_from_text(extractor=extractor)

    def extract_entities_from_document_with_uuid(self, uuid: str, extractor: EntityDocumentExtractor):
        """
        Extracts entities from a document identified by UUID using the provided extractor configuration.

        This method serves as a wrapper around the Extractor's extract_from_document_with_uuid method,
        delegating the actual extraction process to the underlying Extractor instance.

        Args:
            uuid (str): The unique identifier of the document from which to extract entities.
            extractor (EntityDocumentExtractor): A dataclass object containing:
                - matches (str): Specifies the matching criteria for the extraction process.
                - schema (Union[str, dict]): The schema defining the entities to extract.
                If provided as a dict, it will be converted to an indented string by the underlying method.

        Returns:
            Union[dict, list, str]: The extracted entities as a Python object (dict or list) 
                                    if the extraction response is valid JSON, or the raw response string 
                                    if JSON parsing fails.

        Raises:
            TypeError: If the schema in the extractor is not a string or dict.
            Any exceptions that might be raised by the underlying extract_from_document_with_uuid method
            or the API client.

        Note:
            - This method does not modify the input extractor object directly. Any necessary
            preprocessing (such as converting the schema to an indented string) is handled
            by the underlying Extractor class.
            - The actual extraction logic and API communication are handled by the
            _extractor.extract_from_document_with_uuid method.

        Example:
            >>> uuid = "uuid_document"
            >>> extractor = EntityDocumentExtractor(
            ...   matches="protocolo web3",
            ...    schema={
            ...        "networks": []
            ...    }
            ... )
            >>> entities = obj.extract_entities_from_text(uuid, extractor)
            {'networks': ['Polygon', 'Ethereum']}
        """
        return self._extractor.extract_from_document_with_uuid(uuid=uuid, extractor=extractor)

    def get_document_by_uuid(self, uuid: str) -> Document:
        """
        Retrieves a document by its UUID from the API client.

        This method delegates the task of fetching document details based on the provided UUID
        to the API client. It returns a Document object populated with the retrieved data.

        Args:
            uuid (str): The UUID of the document to retrieve.

        Returns:
            Document: A Document object containing the details of the retrieved document.

        Raises:
            APIError: If there is an error in communicating with the API client or parsing the response.
        """
        return self._api_client.get_document_by_uuid(uuid=uuid)

    def search_in_document(self, search: Search) -> SearchDocument:
        """
        Perform a search operation within a document using the provided search parameters.

        This method serves as a wrapper around the API client's search_in_document function,
        delegating the actual search operation to the API client implementation.

        Args:
            search (Search): An instance of the Search class containing the search parameters.
                            This should include all necessary information to perform the search,
                            such as query terms, filters, and any other relevant search criteria.

        Returns:
            SearchDocument: An instance of the SearchDocument class containing the search results.
                            This typically includes matched documents, metadata about the search,
                            and any other relevant information returned by the search operation.

        Raises:
            Any exceptions raised by the underlying API client method will be propagated up
            to the caller of this method.

        Note:
            The actual implementation of the search logic is handled by the API client.
            This method primarily acts as an interface to that functionality within the
            current class or module.

        Example:
            >>> search_params = Search(
            ...     matches="python programming",
            ...     max_results=5,
            ...     uuid="uuid document"
            ... )
            >>> results = integrator.search_in_document(search_params)
            >>> print(f"Found {results.estimatedTotalHits} matches")
            Found 42 matches
            >>> for hit in results.hits[:3]:
            ...     print(f"- {hit.content[:50]}...")
        """
        return self._api_client.search_in_document(search)
