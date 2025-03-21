## Extracting the information with `Unstructured` library
Extracting and chunking information is probably the most important step toward building a RAG model that works well.
Searching the web, I recently found this python library that allows you to extract data from different type of files and 
during the extarction process it also saves really important feature of the metadata, wich make the Retriever more efficient 
as it has more context to look into.

## What kind of data I extracted 
I decided to extract all the data available on the net, so I had to use a function that would extract htlm content. 
Down here you can see the function call

```python
file_paths = 'https://msutexas.edu/about/'
loader = UnstructuredLoader(web_url=file_paths)
docs = loader.load()
```

The best feature of the unstructured library is that the functions used to extract content are able to recognize the different elements
of a html page. This is an example of what I got from the extraction of the [About](https://msutexas.edu/about/) page of MSU

```python
Document(metadata={
  'category_depth': 0,
  'languages': ['eng'],
  'filetype': 'text/html',
  'url': 'https://msutexas.edu/about/',
  'category': 'Title',
  'element_id': '2431404cb722fbecca94eccb81221cb0'
},
page_content='About MSU Texas')
```









