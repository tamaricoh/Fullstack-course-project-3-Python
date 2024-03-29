from pymongo import MongoClient
import requests
import json
import os
import sys
from reader import *
from shelf import *
from book import *
from library import *

# //
# User should create a "books" collection inside "booksDB" database in the localhost

client = MongoClient() 
DB = client["booksDB"]
collection = DB["books"]
collection.insert_one({
    "author" : "Sheldon Axler", 
    "title" : "Linear Algebra Done Right", 
    "num_of_pages" : 340.0
})
collection.insert_one({
    "author" : "Mike Hochman", 
    "title" : "Infinitesimal calculus", 
    "num_of_pages" : 553.0
})
collection.insert_one({
    "author" : "Vikas Swarup", 
    "title" : "Q & A", 
    "num_of_pages" : 304.0
})
collection.insert_one({
    "author" : "Yann Martel", 
    "title" : "Life of Pi", 
    "num_of_pages" : 352.0
})
collection.insert_one({
    "author" : "Dinah Jefferies", 
    "title" : "The Tea Planter's Wife", 
    "num_of_pages" : 448.0
})
collection.insert_one({
    "author" : "Khaled Hosseini", 
    "title" : "The Kite Runner", 
    "num_of_pages" : 371.0
})

# Inserting data to the database
# //

# //
# Creating a library by extracting information from a database

library = library()
booksArr = list(collection.find({}))
for i in range(len(library.shelves)) :
    for j in range(2) :
        bookToAdd = book()
        bookToAdd.author = booksArr[(2*i)+j]["author"]
        bookToAdd.title = booksArr[(2*i)+j]["title"]
        bookToAdd.num_of_pages = booksArr[(2*i)+j]["num_of_pages"]
        library.shelves[i].add_book(bookToAdd)

# //

# //
# Login screen - checking whether the entered user exists

print("LOGGING IN - ")
userName = input("Plaese enter USERNAME : ")
userEmail = input("Plaese enter EMAIL : ")
resp = requests.get("https://jsonplaceholder.typicode.com/users")
users = resp.json()
userNames = list(map(lambda x : x["username"] , users))
emails = list(map(lambda x : x["email"] , users))
if (userName in userNames and userEmail in emails) :
    index1 = userNames.index(userName)
    index2 = emails.index(userEmail)
    logged = index1 == index2
else :
    logged = False

# //

def menu() :
    print("MENU : " + "\n"
    "• For adding a book - Press 1" + "\n" +
    "• For deleting a book - Press 2" + "\n" +
    "• For changing books locations - Press 3" + "\n" +
    "• For registering a new reader - Press 4" + "\n" +
    "• For removing a reader - Press 5" + "\n" +
    "• For searching books by author - Press 6" + "\n" +
    "• For reading a book by a reader - Press 7" + "\n" +
    "• For ordering all books - Press 8" + "\n" +
    "• For saving all data - Press 9" + "\n" +
    "• For loading data - Press 10" + "\n" +
    "• For exit - Press 11" + "\n" 
        )
    option = int(input("Chose option - "))
    print("\n")
    return(option)

while (logged) :
    option = menu()

    if (option == 1) : 
        # Using add_new_book function from 'library' class 
        print("Adding a book \n")
        bookToAdd = book()
        bookToAdd.author = input("Enter author's name : ")
        bookToAdd.title = input("Enter book's title : ")
        bookToAdd.num_of_pages = int(input("Enter number of pages : "))
        library.add_new_book(bookToAdd)

    elif (option == 2) :
        # Using delete_book function from 'library' class 
        print("Deleting a book \n")
        bookTitle = input("Enter book's title : ")
        library.delete_book(bookTitle)

    elif (option == 3) :
        # Using change_locations function from 'library' class 
        print("Changing books locations \n")
        bookA = input("Enter first book title : ")
        bookB = input("Enter second book title : ")
        library.change_locations(bookA , bookB)

    elif (option == 4) :
        # Using register_reader function from 'library' class 
        print("Registering a new reader \n")
        readerName = input("Enter reader's name : ")
        readerID = input("Enter reader's ID : ")
        library.register_reader(readerName , readerID)

    elif (option == 5) :
        # Using remove_reader function from 'library' class 
        print("Removing a reader \n")
        readerName = input("Enter reader's name : ")
        library.remove_reader(readerName)
    
    elif (option == 6) :
        # Using search_by_author function from 'library' class 
        print("Searching books by author \n")
        author = input("Enter author name : ")
        books = library.search_by_author(author)
        print("Books written by " + author + " : ")
        for book in books : 
            print("- " + book)
    
    elif (option == 7) :
        # If instead og readerID the input was readerName - I would've used the 'reader_read_book" function from 'library' class
        print("Reading a book by a reader \n")
        readerID = input("Enter reader's ID : ")
        bookTitle = input("Enter book's title : ")
        for reader in library.readers :
            if (reader.id == readerID) :
                reader.read_book(bookTitle)
                break
        
    elif (option == 8) :
        library.order_books()        

    elif (option == 9) :
        # I created a function called 'to_json()' that returns the data in json as asked
        print("Saving all data \n")
        fileName = input("File name : ")
        with open(os.path.join(sys.path[0], fileName + ".json"),'w') as file :
            data = library.to_json()
            json.dump(data,file)

    elif (option == 10) :
        print("Loading data \n")
        fileName = input("File name : ")
        with open(os.path.join(sys.path[0], fileName + ".json"),'r') as file :
            data = json.load(file)
            for i in range(len(data["shelves"])) :
                library.shelves[i].is_shelf_full = data["shelves"][i]["is_shelf_full"]
                for book in data["shelves"][i]["books"] :
                    bookToAdd.author = book["author"]
                    bookToAdd.title = book["title"]
                    bookToAdd.num_of_pages = book["num_of_pages"]
                    library.shelves[i].books.append(bookToAdd)
            for readerJson in data["readers"] :
                readerToAdd = reader()
                readerToAdd.id = readerJson["id"]
                readerToAdd.name = readerJson["name"]
                readerToAdd.books = readerJson["books"]
                library.readers.append(readerToAdd)

    elif (option == 11) :
        exit()
    
    print("\n \n \n")
