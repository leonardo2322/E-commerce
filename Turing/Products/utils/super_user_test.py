from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render

class Super_user_is(UserPassesTestMixin):
    
    def test_super_user(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        # Redirigir al usuario si no tiene permiso
        return render(self.request, '403.html', status=403)