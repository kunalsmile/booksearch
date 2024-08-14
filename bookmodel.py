class BookModel:

    def __init__(self):
        pass

    title = ""
    subTitle = ""
    selfLink = ""
    authors = ""
    publisher = ""
    publishedDate = ""
    description = ""
    industryIdentifiers = ""
    imageLinks = ""
    language = ""
    previewLink = ""
    searchInfo = ""
    categories = ""
    googleId = ""
    flipkartId = ""
    languageKey = 0
    publisherKey = 0
    pageCount = 0
    printType = ""
    ageGroup = ""

    def getPublisher(self):
        return self.publisher.strip()

    def getLanguage(self):
        return self.language.strip()