# ind_study
Independent Study Research on the development of a RAG model over MSU texas information

## Extracting the information with `Unstructured` library
Extracting and chunking information is probably the most important step toward building a RAG model that works well.
Searching the web, I recently found this python library that allows you to extract data from different type of files and 
during the extarction process it also saves really important feature of the metadata, wich make the Retriever more efficient 
as it has more context to look into.

## What kind of data I extracted 
I decided to extract all the data available on the net, so I had to use a function that would extract htlm content. 
Down here you can see the function call

```python
elements_url = partition_html(url = "https://msutexas.edu/about/")
```

The best feature of the unstructured library is that the functions used to extract content are able to recognize the different elements
of a html page. This is an example of what I got from the extraction of the [About](https://msutexas.edu/about/) page of MSU

```json
{
    "type": "Title",
    "element_id": "2431404cb722fbecca94eccb81221cb0",
    "text": "About MSU Texas",
    "metadata": {
      "category_depth": 0,
      "languages": [
        "eng"
      ],
      "filetype": "text/html",
      "url": "https://msutexas.edu/about/"
    }
  }
```











# Using Langchain to load web pages
LangChain is a framework designed to simplify the development of applications that use large language models (LLMs) by providing tools for retrieval, memory, and chaining. It helps developers build chatbots, RAG applications, agents, and automation tools by integrating LLMs with external data sources, APIs, and databases. 

## `Document` object
When extracting content from web pages, Langchain gives back a `Document` object that consist of key value pair: content (the actual text and information extracted) and a metadata which provides information about where the content was extracted. The metadata could be really simple or a little more detailed. Here are some examples: 
### Simple Document
```python
document = Document(
    page_content="Hello, world!",
    metadata={"source": "https://example.com"}
)
```
### Advanced Document
```python
Document(metadata={'source': './example_data/layout-parser-paper.pdf', 'coordinates': {'points': ((16.34, 213.36), (16.34, 253.36), (36.34, 253.36), (36.34, 213.36)), 'system': 'PixelSpace', 'layout_width': 612, 'layout_height': 792}, 'file_directory': './example_data', 'filename': 'layout-parser-paper.pdf', 'languages': ['eng'], 'last_modified': '2024-02-27T15:49:27', 'page_number': 1, 'filetype': 'application/pdf', 'category': 'UncategorizedText', 'element_id': 'd3ce55f220dfb75891b4394a18bcb973'}, page_content='1 2 0 2')
```

Let's start with the simple extraction. The library we will need are `langchain-community` and `beautifulsoup4`. For my project I will try to extract the https://msutexas.edu/about/ web page.
We frist import the libraries:
```python
import bs4
from langchain_community.document_loaders import WebBaseLoader
```
Then we copy the url from the web page
```python
page_url = 'https://msutexas.edu/about/'
```
Then we load the content of the page with the `WebBaseLoader` package and `alazy_load`
```python
loader = WebBaseLoader(web_paths=[page_url])
docs = []
async for doc in loader.alazy_load():
    docs.append(doc)
```
And this is what we get back for the `metadata`
```python
{
    'source': 'https://msutexas.edu/about/',
    'title': '\r\n\t\t\tAbout MSU Texas »MSU Texas »\r\n\t\t',
    'description': 'General information about MSU and the campus.',
    'language': 'en'
}
```
And this is are the first 250 character of the `page_content`
```python
'\n\n\n\n\n\n\n\r\n\t\t\tAbout MSU Texas »MSU Texas »\r\n\t\t\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nSkip to main content\n\n\n\n \n\n\n\n\n\n\nLogin\n\n\nmyMSUTexas\nD2L\nFaculty/Staff E-mail\n\n\n\n\n  \nSearch MSU Texas\n Search  \n\n\n\n\nApply\nAlumni\nFaculty & Staff\nDirectory\nMa'
```
As you can see the `page_content` value is filled with extra carhacter that we don't need to embed and store in the database. Said so, we need further parsing on the content so that all the content is omogenous and ready to be split in chunks. In order to get a more omegenous text we'll have to change a couple of parameters in the `WebBaseLoader` function
```python
loader = WebBaseLoader(
    web_paths=[page_url],
    bs_get_text_kwargs={"separator": " | ", "strip": True},
)
```
In this case the `bs_get_text_kwargs` paramater takes in a `separator` that will divide each block of text with a vertical bar and `strip = True` which removes leading and trailing whitespace. And this is the new output:
```python
'About MSU Texas »MSU Texas » | Skip to main content | Login | myMSUTexas | D2L | Faculty/Staff E-mail | Search MSU Texas | Search | Apply | Alumni | Faculty & Staff | Directory | Map | Athletics | Registrar | Academic Calendar | Address Changes | Class Schedule | Apply for Graduation | Commencement | Texas Success Initiative | Transcripts - How to Order | University Catalogs | Veterans Affairs | WebWorld: Registration, Grades, Payments, etc. | Registrar Homepage | Student Life | About MSU | Admissions | Undergraduate | Graduate | Global Education | Admissions Homepage | Academics | MSU Texas Homepage | Menu | Home | About MSU Texas | About MSU Texas | Why MSU Texas | Midwestern State University (MSU Texas) is a public university in Wichita Falls, Texas. We are a small and mighty community of Mustangs, with an average class size of just 30 students, 75+ degree programs to choose from'
```
The parsed content looks definetely better and cleaner but since RAG models are based on semantic search or in simpler term they retrieve the information that looks closer to the query, all those phrases like: Skip to main content, myMSUTexas, Faculty & Staff etc.. they will only make the retrivier job harder lowering the accuracy and efficency of the RAG system. 

Our next goal is to extract only information that are relevant. I noticed that all the unrelevant piece of content are under either a `<a>` tag or a `<href>` so I tried to modify some paramaters of the `WebBaseLoader` function but unfortunately I did not find a way to do that. I tried to use the `BeautifulSoup(doc.page_content, "lxml")` that gives you back that html page with tags as well. This is the output:
```python
<html><body><p>About MSU Texas »MSU Texas » | Skip to main content | Login | myMSUTexas | D2L | Faculty/Staff E-mail | Search MSU Texas | Search | Apply | Alumni | Faculty &amp; Staff | Directory | Map | Athletics | Registrar | Academic Calendar | Address Changes | Class Schedule | Apply for Graduation | Commencement | Texas Success Initiative | Transcripts - How to Order | University Catalogs | Veterans Affairs | WebWorld: Registration, Grades, Payments, etc. | Registrar Homepage | Student Life | About MSU | Admissions | Undergraduate | Graduate | Global Education | Admissions Homepage | Academics | MSU Texas Homepage | Menu | Home | About MSU Texas | About MSU Texas | Why MSU Texas | Midwestern State University (MSU Texas) is a public university in Wichita Falls, Texas. We are a small and mighty community of Mustangs, with an average class size of just 30 students</p></body></html>
```
As you can notice it doesn't go deep enouhg into `<a>` and `<href>` tags and it puts everything togeter under the `<p>` tag. So I found another way to extract the raw HTML content combining the `request` and the `BeautifulSoup` libraries. Here is the code:
```python
url = "https://msutexas.edu/about/"  
headers = {"User-Agent": "Chrome/110.0.0.0"}

response = requests.get(url, headers=headers)
html_content = response.text

soup = BeautifulSoup(html_content, "lxml")
```
And this is some of the output:
```python
<!DOCTYPE html>
<html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8"/>
<meta content="IE=edge" http-equiv="X-UA-Compatible"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<meta content="c1a657c90a0008483af171afffc0d6ab" name="id"/>
<title>
			About MSU Texas »MSU Texas »
		</title>
<meta content="about" name="keywords"/>
<meta content="General information about MSU and the campus." name="description"/>
<link href="https://msutexas.edu/about/" rel="canonical"/>
<link as="style" href="../_assets/css/fonts.css"/>
<link as="style" href="../_assets/css/tw/components.css"/>
<link href="/_assets/css/site.css?v=1734642322633" rel="stylesheet"/>
<link href="../_assets/favicons/apple-touch-icon-57x57.png" rel="apple-touch-icon-precomposed" sizes="57x57"/>
<link href="../_assets/favicons/apple-touch-icon-114x114.png" rel="apple-touch-icon-precomposed" sizes="114x114"/>
<link href="../_assets/favicons/apple-touch-icon-72x72.png" rel="apple-touch-icon-precomposed" sizes="72x72"/>
<link href="../_assets/favicons/apple-touch-icon-144x144.png" rel="apple-touch-icon-precomposed" sizes="144x144"/>
<link href="../_assets/favicons/apple-touch-icon-60x60.png" rel="apple-touch-icon-precomposed" sizes="60x60"/>
<link href="../_assets/favicons/apple-touch-icon-120x120.png" rel="apple-touch-icon-precomposed" sizes="120x120"/>
<link href="../_assets/favicons/apple-touch-icon-76x76.png" rel="apple-touch-icon-precomposed" sizes="76x76"/>
<link href="../_assets/favicons/apple-touch-icon-152x152.png" rel="apple-touch-icon-precomposed" sizes="152x152"/>
<link href="../_assets/favicons/favicon-196x196.png" rel="icon" sizes="196x196" type="image/png"/>
<link href="../_assets/favicons/favicon-96x96.png" rel="icon" sizes="96x96" type="image/png"/>
<link href="../_assets/favicons/favicon-32x32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="../_assets/favicons/favicon-16x16.png" rel="icon" sizes="16x16" type="image/png"/>
<link href="../_assets/favicons/favicon-128.png" rel="icon" sizes="128x128" type="image/png"/>
```
Now that we have all the tags available we can proceed and eliminate the one that we actually don't need. 
```python
for a_tag in soup.find_all(['a','button']):
    a_tag.decompose()  # Deletes links
clean_text = soup.get_text(separator=" | ", strip=True)
```
This 3 lines of code helped me getting rid of the tags that contained irrelevant information. This is now the clean output:
```python
About MSU Texas »MSU Texas » | About MSU Texas | Why MSU Texas | Midwestern State University (MSU Texas) is a public university in Wichita Falls, Texas. We are a small and mighty community of Mustangs, with an average class size of just 30 students, 75+ degree programs to choose from, and an opportunity-rich location halfway between Oklahoma City and the Dallas-Fort Worth metroplex. Our | unites us so that you will be supported to be your best in all you set out to do. | Anchor links to help you more quickly navigate the MSU Texas About Us webpage. | More Info | More Info | Find Your Place on Our Unique Campus | Mustangs are scientists and artists. Athletes and bookworms. Texas natives and students from places all over the map. You will find your space and your place here as a member of the Mustangs community. And no matter where you are coming from or where you want to go next, you will find success with our support. | Meet President Stacia Haynie, Ph.D. | Hello there! MSU Texas has been home for me since I first set foot on campus as an undergraduate student. In fact, it is where I found the support and encouragement I needed to reach my goals. I cannot wait to welcome you to find your own place here with us. | 16:1 | Student-to-Faculty Ratio:
```
Now that I have a clean content that conatains basically only useful information I can creates documents objects with as metadata the url. Here the code:
```python
docs = Document(
    page_content=clean_text,
    metadata = {'source': url}
)
```
after having created the document object we can go ahead and split the text into chunks so that we can embed each chunks. In order to accomplish this step I will be using the `RecursiveCharacterTextSplitter` class by langchain. The `RecursiveCharacterTextSplitter` uses a recursive splitting strategy based on a list of separators, breaking the text at the largest possible chunk size while respecting logical text boundaries (like paragraphs, sentences, or words).
```python
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=20
    )
splits = splitter.split_documents([docs])
```
`from_tiktoken_encoder` is a class method that initializes the `RecursiveCharacterTextSplitter` using a token-based approach instead of a character-based one. Instead of measuring characters (which can vary in byte size), this method counts tokens, making it better suited for token-limited models like OpenAI’s GPT-4.
The `chunk_size` parameters indicates how many tokens can a single chunk contains at most, while the `chunk_overlap` ensures some overlap between consecutive chunks, preventing loss of context when breaking text.

## Langchain `Unstructured` web scraping


