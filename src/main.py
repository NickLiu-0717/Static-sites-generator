from textnode import TextNode
from htmlnode import *

def main(): 
    textnode1 = TextNode("This is a text node", "bold", "https://www.boot.dev")
    textnode2 = TextNode("click here", "link", "https://www.boot.dev")
    # print(textnode1 == textnode2)

    
main()