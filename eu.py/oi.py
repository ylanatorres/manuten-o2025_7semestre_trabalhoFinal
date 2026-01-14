def perform_update(self, serializer):
    serializer = CinemaSerializer(data=self.request.data) 
    if serializer.is_valid():
        serializer.save()
        
        
        
def login(request):
    token_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ..."
    return Response({"token": token_jwt})


def test_login_admin(self):
    client = APIClient()
    credentials = ('admin_user', 'senha_super_secreta_123') 
    response = client.post('/login/', auth=credentials)
    

def get_external_data(self):
    headers = {
        'Authorization': 'Bearer 12345-token-fixo-inseguro'
    }
    requests.get('https://api.externa.com', headers=headers)
    
    
    
class Cinema(models.Model):
    name = models.CharField(max_length=255, null=True) 
    description = models.CharField(max_length=500, null=True)
    
    
def check_status(self):
    if self.request.user.is_active:
        pass 
    
    try:
        self.save()
    except Exception:
        pass