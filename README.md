# Internship Journey

This repository documents my whole internship journey including daily tasks,learning progress,my skillsand projects and also experiences.

---

## Python_OOP_and_Django_internals Branch

### Company information 
- Company Name: উপায়(UCB Fintech Company Ltd)
- Position: Software Engineer Intern(Backend)
- Department: Tech Division
- Duration: 13 May 2026 - Present

---
### First three task 
1. Read Python OOP docs — classes,object,Encapsulation, inheritance,Abstruction,dunder methods, decorators, generators. create a python file having everything you learned.
2. Build custom Django middleware that logs request time, IP, and user agent to a file.
3. Read Django source code — how HttpRequest travels from wsgi to view to client. Write a 1-page explanation(in markdown) in your own word 
---



How an HTTP Request travels in Django: From WSGI to View to Client

In django evey web request mainly follow a structured rule or flow from the clint http request to the Django and back response from the appilication and it is managed by the WSGI stands for(Web server gateway interface) then Django multi level middleware thenn Url routing take to the correct vies that matches and then back the reponse then again run the middleware and wsgi to the view


here have multiple point -

1. Firstly a user send a request using his browser by hitting a url. The user can hit url as his wants in many ways he want.

2. After hiting the urls by the WSGI server receive the request.When i run the django appilication it run on multiple WSGi server like that Gunicorn , django development server and more. The wsgi server mainly work between the django appilication and the web server. the wsgi parse the raw http request into a proper HttP request formet and then it pass it for the django handler.

3. in django the request handler that store in the wsgi.py file and it contain the callble funbctions. So the hander in wsgi call function with two aggument.
     - environ : contain all the request data including headers,path, method, query, server info.
     - then start a start response function with callback

4. after this start a middleware( request middleware) - Before reach the view the request pass through multi  layer middleware( that include on the list it can be existing or custom middleware). It can modify the request,block request if not match the condition also add data,loog request,store login details,authentical,role check, session and so on. so it work in middle.

5. After the middleware the request comes in the urls.py and check with path match.if match with any then pass it to the view.py to execute the logic and if not match its gives a error with 404.l

6. In views check first with function or logic match with it, then run the business logic if need connect with the database after all the process and logic run the output context is ready to pass.\

7. The view return the HTTP response and send back the response to the response middleware the response can be multiple type like json ,html file etc

8. Then the response take the response middileware.Before sending the response to the client middlewsre can do many thing - modify the response,add information,store cookie, store the log information and so on.

9. after processing complete of the response middleware django send the http response to the wsgi server . the wsgu server convert the http response to user friendly raw html formet

10. then the browser receive the response and render ir or show the raw data. in the processing if any error occurs it can return error value 


