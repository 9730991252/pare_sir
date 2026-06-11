from django.shortcuts import render
from core.models import UnderConstruction

class UnderConstructionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        path = request.path.strip('/')
        
        # Explicitly allow homepage
        if request.path == '/':
            return self.get_response(request)
        
        allowed_paths = [
            'super_admin',
            'college_login',
            'logout',
            'static',
            'media',
        ]
        
        is_allowed = any(path.startswith(allowed) for allowed in allowed_paths)
        
        if not is_allowed:
            try:
                uc = UnderConstruction.objects.first()
                if uc and uc.status == 1:
                    return render(request, 'under_construction.html')
            except Exception:
                pass
        
        return self.get_response(request)