import requests
from lxml import html


class Part:
    def __init__(self, partNumber, description, MSRP):
        self.partNumber = partNumber
        self.description = description
        self.MSRP = MSRP

class Engine:
    def __init__(self, modelNumber):
        self.baseURL = "http://www.marineengine.com/parts/johnson-evinrude-models.php?model_number="
        self.modelNumber = modelNumber
        self.horsePower = None
        self.year = None
        self.partsCategories = None
        self.partsList = []

        try:
            depthScrape = requests.get((self.baseURL + self.modelNumber), timeout=10)
            subTree = html.fromstring(depthScrape.content)
            self.year = subTree.xpath('/html/body/main/div[1]/p/a[2]/text()[normalize-space()]')
            self.horsePower = subTree.xpath('/html/body/main/div[1]/p/a[3]/text()[normalize-space()]')
            print(self.horsePower)
            print(self.year)
            self.partsCategories = subTree.xpath('//tr/td/div[1]/div[2]/ul/li/a/@href')
            for element in self.partsCategories:
                print(element)
                depthScrape = requests.get("http://www.marineengine.com" + element, timeout=10)
                subTree = html.fromstring(depthScrape.content)
                newListingInfo = subTree.xpath('//tr[2]/td[3]/p[1]/small/a/@href')
                unavailableListingInfo = subTree.xpath('//tr[2]/td[3]/small[1]/a/@href')
                newListingInfo = unavailableListingInfo + newListingInfo
                for item in newListingInfo:
                    depthScrape = requests.get("http://www.marineengine.com" + item, timeout=10)
                    subTree = html.fromstring(depthScrape.content)
                    newListing = subTree.xpath('//html/body/main/h1/text()')[0].replace('\n', ' ').split("-")
                    if len(newListing) == 1:
                        newListing = newListing[0].replace('\n', '').split(":")

                    newListingMSRP = subTree.xpath('/html/body/main/div[2]/div[1]/div[4]/div[2]/p/text()')
                    newPart = Part(newListing[0].strip(), newListing[1].strip(), newListingMSRP)
                    print("_________________________")
                    print(newPart.description)
                    print(newPart.partNumber)
                    print(newPart.MSRP)
                    print("_________________________")
                    self.partsList.append(newPart)


            print("Total parts: ", len(self.partsList))
                # Go through each page and pull as many part numbers as possible. Put these in 'partsList'
                # Then go search all of them on ebay and see if anything is worth a lot
                # Return results in descending order of expected value (with unknowns at the bottom)

        except requests.exceptions.RequestException as e:
            print("Connection error:", e)


engine = Engine("4536a")
engine = Engine("135ETL75E")
