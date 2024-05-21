## Title: The Keen Observer

## Details:
* difficulty: Hard
* category: Web 
* author: Sarmed
* flags: flag{trail_is_the_answer}

## Description:
This challenge is based on a real-world scenario where the process of finding vulnerabilities during penetration testing phase and exploiting them to extract sensitive information is implemented.

## Hint:
Follow the path and you'll find the secrets that lie therein.

## Intended Learning and outcome:
1. What is directory busting and the tools that are used for it.
2. What is robots.txt file.
3. What is server-side request forgery.
4. What is git and ways to find important information inside .git file.
5. Understanding the damage .git file can cause if it's leaked.

## Solution: 
When we begin the challenge, we are shown a web application that contains a file upload and download operation. We try to look for any hints but can't find anything. We then proceed to perform directory busting, this can be done using different tools, we use dirb, and find that robots.txt route is present. We go to the route and find a hint that there is something on the route **/vulnerability?url=**.
This can mean multiple vulnerabilities including open redirection, cross site scripting, etc. We are successful in exploiting SSRF and notice that a file by the name of git.zip is downloaded. Extracting it, we find a .git file inside it and using git commands we can see that it is this project's git file. We see commits inside it and find there are many commits but 3 are by someone named The Keen Observer. In one of the commit, there is data which looks like it's encrypted. There are another two commits by the name of Hint and Hint 2, we use git diff on them and see that the data we saw earlier was encrypted using Ceaser's cipher with a subtitution of 3 alphabets forward. We decrypt the text and find the flag.


........




