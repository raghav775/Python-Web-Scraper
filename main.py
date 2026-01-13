import requests
from bs4 import BeautifulSoup
import csv

url = input("Enter the URL of the webpage you want to scrape: ")
# fetch the webpage
try:
    response = requests.get(url)
    response.raise_for_status() # Raise an error acc to response
except requests.exceptions.RequestException as e:
    print("Error fetching the webpage:", e)
    exit()

choice = input("Enter what you want to extract \n1.title\n2.headings\n3.Paragraphs\n4.links\nEnter Your Choice:").lower()

# something to store the data in 
output_data = []

# check if beautifulsoup the html parser for our project is succesfuly loaded
if response.status_code == 200:
    soup = BeautifulSoup(response.text,"html.parser")

# extracting all titles from the webpage
    if choice == "1":
        title = soup.title.text if soup.title else "No title found"
        print("\nPage Title:", title)
        output_data.append(f"Page Title: {title}")   
        
# extracting all headings h1, h2, h3 and putting them in a loop
    elif choice == "2":
        headings = soup.find_all(["h1","h2","h3"])
        print("\nHeadings:")
        for h in headings:
            text = h.get_text(strip=True)
            print("-", h.text.strip())
            output_data.append(f"heading: {text}")

    elif choice == "3":
        paragraphs = soup.find_all("p")
        for p in paragraphs:
            text = p.get_text(strip=True)
            print("-", text)
            output_data.append(f"paragraph: {text}")

# extracting all links and putting them in a loop
    elif choice == "4":
        links = soup.find_all("a")
        print("\nLinks:")
        for link in links:
            href = link.get("href")
            if href:
                print("-",href)
                output_data.append(f"link: {href}")
    else:
        print("Invalid choice. Please select from title, headings, links.")
        exit()
else:
    print("Failed to fetch the webpage. Status code:", response.status_code)

# take input of filename
filename = input("Enter the filename to save the output in (without .txt):")
if not filename:
    if choice == "1":
        filename = "titles"
    elif choice == "2":
        filename = "headings"
    elif choice == "3":
        filename = "paragraphs" 
    elif choice == "4":
        filename = "links"
        
# take input of search keyword
search_query = input("Enter a keyword to filter results (or press Enter to skip): ").lower()
if search_query:
    output_data = [line for line in output_data if search_query in line.lower()]
if not output_data:
    print("No data found matching your keyword.")
else:
    print(f"\nFound {len(output_data)} matching results!")

# take input of filetype
filetype = input("Enter the file type to save the output (txt/csv): ").lower()
if filetype == "csv":
    filename = filename + ".csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if choice == "2":
            writer.writerow(["Heading"])
            for line in output_data:
                    writer.writerow([line])
        else:
            writer.writerow(["Content"])
            for line in output_data:
                writer.writerow([line])
else:
    filetype = "txt"
    filename = filename + ".txt"
    with open(filename,"w", encoding= "utf-8") as f:
        for line in output_data:
            f.write(line + "\n")
print(f"Data has been written in '{filename}' successfully.")