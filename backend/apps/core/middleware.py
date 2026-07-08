"""
Middleware para sesiones múltiples por pestaña
Permite tener diferentes usuarios en diferentes pestañas del navegador
"""


class MultiTabSessionMiddleware:
    """
    Middleware que permite sesiones independientes por pestaña del navegador
    usando sessionStorage del lado del cliente
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Obtener tab_id del POST, GET, o COOKIES
        tab_id = request.POST.get('tab_id') or request.GET.get('tab_id') or request.COOKIES.get('tab_id')
        
        # Si hay tab_id, usar sesiones por pestaña
        # Si NO hay tab_id, usar sesión normal (compatibilidad)
        if tab_id:
            # Guardar el tab_id en la request para usarlo en las vistas
            request.tab_id = tab_id
            
            # Prefijo para las claves de sesión específicas de esta pestaña
            prefix = f'tab_{tab_id}_'
            
            # Crear un wrapper para session que use el prefijo
            original_session = request.session
            request._original_session = original_session
            
            class TabSession:
                def __init__(self, session, prefix):
                    self._session = session
                    self._prefix = prefix
                
                def get(self, key, default=None):
                    return self._session.get(self._prefix + key, default)
                
                def __getitem__(self, key):
                    return self._session[self._prefix + key]
                
                def __setitem__(self, key, value):
                    self._session[self._prefix + key] = value
                
                def __delitem__(self, key):
                    del self._session[self._prefix + key]
                
                def __contains__(self, key):
                    return (self._prefix + key) in self._session
                
                def flush(self):
                    # Eliminar solo las claves de esta pestaña
                    keys_to_delete = [k for k in self._session.keys() if k.startswith(self._prefix)]
                    for k in keys_to_delete:
                        del self._session[k]
                
                def setdefault(self, key, default=None):
                    return self._session.setdefault(self._prefix + key, default)
            
            # Reemplazar temporalmente la sesión
            request.session = TabSession(original_session, prefix)
        
        response = self.get_response(request)
        
        # Restaurar la sesión original si fue modificada
        if hasattr(request, '_original_session'):
            request.session = request._original_session
        
        return response
