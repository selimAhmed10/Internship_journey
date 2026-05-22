from datetime import datetime

class RequestLogMiddleware:   #define class for collect the info in log
    
    def __init__(self,get_response):  #initialize one when run the middleware
        self.get_response=get_response
        
    def __call__(self, request):
        # before the view do all operations that need , call every time for every request
        
        time=datetime.now()
        ip_address=request.META.get("REMOTE_ADDR")
        user_agent=request.META.get("HTTP_USER_AGENT",'Unknown')
        
        log=(
            f"Time:{time} -- " f"IP:{ip_address} -- " f"User agent: {user_agent}\n"
        )
        
        with open("request_logs.txt", "a") as file:
            file.write(log)
            
        response=self.get_response(request)   #for manage continue request
        return response