import time
import datetime
import os
import json

class APITrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        start_time=time.perf_counter()
        response=self.get_response(request)
        if request.path.startswith('/api/'):
            execution_time=(time.perf_counter()-start_time)*1000
            user=request.user.username if request.user and request.user.is_authenticated else "Anonymous"
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0].strip()
            else:
                ip_address =request.META.get('REMOTE_ADDR','Unknown IP')
                
            browser_info=request.META.get('HTTP_USER_AGENT','Unknown Browser')
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log = (
                f"[{timestamp}] "
                f"User: {user} | "
                f"Method: {request.method} | "
                f"Path: {request.path} | "
                f"Status: {response.status_code} | "
                f"Time in mili second: {execution_time:.2f}ms | "
                f"IP: {ip_address} | "
                f"Browser: {browser_info}\n"
            )
            with open("logs/api_tracking.txt", "a", encoding="utf-8") as file:
                file.write(log)
                
        return response
