import requests
import streamlit as st

from bookmodel import BookModel

books = []

st.set_page_config(
    page_title="Book Search",
    page_icon="book",
)

st.header("Book Search")

st.text_input("Enter your search keyword", key="keyword")

def prepareList():
    results = getSearchResult()
    for item in results["items"]:
        book = populateBookModel(item)
        books.append(book)


def getSearchResult():
    return requests.get("https://www.googleapis.com/books/v1/volumes?q=" + st.session_state.keyword + "&country=US").json()


def getSelectedCheckboxes():
    keys = []
    for key in st.session_state:
        if key.startswith("dynamic_checkbox_") and st.session_state[key]:
            keys.append(key)
    return keys


def getAuthors(authors):
    returnValue: str = ""
    for author in authors:
        returnValue += author + "|"
    # st.write(returnValue)
    return returnValue


def getImageLinks(imageLinks):
    returnValue: str = ""
    for link in imageLinks:
        if "smallThumbnail" in imageLinks:
            returnValue += "st^" + imageLinks["smallThumbnail"] + "|"
        if "thumbnail" in imageLinks:
            returnValue += "th^" + imageLinks["thumbnail"] + "|"
        if "small" in imageLinks:
            returnValue += "sm^" + imageLinks["small"] + "|"
        if "large" in imageLinks:
            returnValue += "la^" + imageLinks["large"] + "|"
        if "medium" in imageLinks:
            returnValue += "md^" + imageLinks["medium"] + "|"
        if "extraLarge" in imageLinks:
            returnValue += "el^" + imageLinks["extraLarge"] + "|"
    # st.write(returnValue)
    return returnValue


def getIndustryIdentifiers(industryIdentifiers):
    returnValue = ""
    for industryIdentifier in industryIdentifiers:
        if industryIdentifier["type"] == "ISBN_10":
            returnValue += "ISBN_10:" + industryIdentifier["identifier"] + "|"
        if industryIdentifier["type"] == "ISBN_13":
            returnValue += "ISBN_13:" + industryIdentifier["identifier"] + "|"
    # st.write(returnValue)
    return returnValue

def getCategories(categories):
    returnValue = ""
    # for category in categories:


def populateBookModel(item):
    volumeInfo = item["volumeInfo"]
    book = BookModel()

    if "title" in volumeInfo:
        book.title = volumeInfo["title"].replace("'", "")
    if "subtitle" in volumeInfo:
        book.subTitle = volumeInfo["subtitle"].replace("'", "")
    if "selfLink" in item:
        book.selfLink = item["selfLink"]
    if "authors" in volumeInfo:
        # book.authors = volumeInfo["authors"]
        book.authors = getAuthors(volumeInfo["authors"])
    if "publisher" in volumeInfo:
        book.publisher = volumeInfo["publisher"].strip().replace("'", "")
    if "publishedDate" in volumeInfo:
        book.publishedDate = volumeInfo["publishedDate"].strip()
    if "description" in volumeInfo:
        book.description = volumeInfo["description"].replace("'", "")
    if "industryIdentifiers" in volumeInfo:
        # book.industryIdentifiers = volumeInfo["industryIdentifiers"]
        book.industryIdentifiers = getIndustryIdentifiers(volumeInfo["industryIdentifiers"])
    if "imageLinks" in volumeInfo:
        book.imageLinks = volumeInfo["imageLinks"]
    if "language" in volumeInfo:
        book.language = volumeInfo["language"].strip()
    if "previewLink" in volumeInfo:
        book.previewLink = volumeInfo["previewLink"]
    if "searchInfo" in item:
        book.searchInfo = item["searchInfo"]["textSnippet"].replace("'", "")
    if "categories" in volumeInfo:
        book.categories = volumeInfo["categories"]
    if "pageCount" in volumeInfo:
        book.pageCount = volumeInfo["pageCount"]
    book.googleId = item["id"].strip()

    # if len(book.selfLink) > 0:
    #     bookInfo = requests.get(book.selfLink).json()
    #     volumeBookInfo = bookInfo["volumeInfo"]
    #     if "imageLinks" in volumeBookInfo:
    #         book.imageLinks = volumeBookInfo["imageLinks"]
    #         # book.imageLinks = getImageLinks(volumeInfo["imageLinks"])
    #     if "categories" in volumeBookInfo:
    #         book.categories = volumeBookInfo["categories"]
    return book


if not (st.session_state.keyword == ""):
    prepareList()


def displayBooks():
    global title, description, subTitle, image
    if len(books) > 0:
        title, thumbnail, description, authorName, subTitle = "", "", "", "", ""
        for book in books:
            if len(book.title) > 0:
                title = book.title
            if len(book.subTitle) > 0:
                subTitle = book.subTitle
            if len(book.description) > 0:
                description = book.description
            if len(book.imageLinks) > 0:
                if "thumbnail" in book.imageLinks:
                    thumbnail = book.imageLinks["thumbnail"]
            if len(book.authors) > 0:
                authorName = book.authors[0]
            with st.container():
                # st.checkbox(book.title, key='dynamic_checkbox_' + book.googleId)
                st.header(title)
                st.write(subTitle)
                image, author = st.columns(2)
                with image:
                    st.image(thumbnail)
                with author:
                    st.html("<b>Author: </b>" + authorName)
                    st.html("<b>Publisher: </b>" + book.publisher)

                    st.write(book.searchInfo)
                with st.expander("Summary"):
                    st.write(description)
                st.divider()


displayBooks()
