from docling.document_converter import DocumentConverter

# source = "https://arxiv.org/pdf/1706.03762"

class DocumentProcessor():
    def __init__(self):
        """
        Initialize the DocumentConverter with a DocumentConverter object.

        This is a hack to get the object to work with the current structure of
        the codebase. In the future, it should be refactored to use a more
        standard structure.
        """
        self.converter = DocumentConverter()

    def convertpdf(self, source_url):
        """
        Given a source_url, download the document and export to markdown.

        Parameters
        ----------
        source_url : str
            The URL of the document to be downloaded and converted to markdown.

        Returns
        -------
        str
            The markdown-ified document.
        """
        result = self.converter.convert(source_url)
        return result.document.export_to_markdown()