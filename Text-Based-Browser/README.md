# About

Having the option to read online documentation or find something on the Internet from the command line or terminal can really come in handy. Let's use Python to create a text-based browser. In this project, you will create a simplified browser that will ignore JS and CSS, won't have cookies, and only will show a limited set of tags. 
But it will still be good enough for some situations, and building it will be fun!

# Learning outcomes

In this project, you will learn how HTTP works and how to work with it in Python. You will become familiar with Python input and output. You will also need to parse HTML, so you'll get some experience with that, too.


Description

Every browser accepts a string from the user and then displays a web page. The string from the user is a URL (Uniform Resource Locator) and looks something like this: https://www.google.com. After receiving the URL, the browser has a lot of work to do, but in a nutshell, this work can be described as finding the web page. The web page is located somewhere on the Internet, and the browser has to retrieve it. Since the https://www. part is always the same, it is often omitted and the link is shortened to google.com.

allow browser to store web pages in a file and show them if the user types a shortened request (for example, wikipedia instead of wikipedia.org). You can store each page as a separate file or find another way to do this. Your program should accept one command-line argument, which is a directory to store the files, and the web pages should be saved inside this directory.

Every browser has a “back” button. If the user presses this button, the browser shows the previous web page. This feature can be implemented using a stack. This will allow the browser to save the pages visited by the user – google, wikipedia, bloomberg, … – but when the user types back, you will see the pages in the reverse order – … bloomberg, wikipedia, google.


Now we should bring our browser closer to resembling a real one by adding an address bar. In this stage, you need to leave your hard-coded variables behind and show your user some real pages. Make the browser request real input URLs and display the results.

You might find that you suddenly don't have permission to visit certain websites. That’s because of the user-agent, which is just a string that all browsers use to mark the request. Browsers have different user-agents, and since yours doesn’t have one, it may encounter problems. Frankly, browsers add a lot of additional information to the requests. All this info can be set using the request library. For this task, it's optional, but feel free to experiment.
