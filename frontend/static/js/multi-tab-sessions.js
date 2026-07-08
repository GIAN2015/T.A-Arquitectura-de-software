/**
 * Sistema de Sesiones Múltiples por Pestaña
 * Permite tener diferentes usuarios logueados en diferentes pestañas
 */

(function() {
    'use strict';
    
    // Generar o recuperar ID único para esta pestaña
    function getTabId() {
        let tabId = sessionStorage.getItem('tabId');
        if (!tabId) {
            tabId = 'tab_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem('tabId', tabId);
        }
        return tabId;
    }
    
    // Agregar tabId a todos los formularios
    function injectTabId() {
        const tabId = getTabId();
        
        // Agregar a todos los formularios
        document.querySelectorAll('form').forEach(form => {
            // Solo si no tiene ya el campo
            if (!form.querySelector('input[name="tab_id"]')) {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'tab_id';
                input.value = tabId;
                form.appendChild(input);
            }
        });
        
        // Agregar a todos los enlaces con método POST (si existen)
        document.querySelectorAll('a[data-method="post"]').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = this.href;
                
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = document.querySelector('[name=csrfmiddlewaretoken]').value;
                
                const tabInput = document.createElement('input');
                tabInput.type = 'hidden';
                tabInput.name = 'tab_id';
                tabInput.value = tabId;
                
                form.appendChild(csrfInput);
                form.appendChild(tabInput);
                document.body.appendChild(form);
                form.submit();
            });
        });
    }
    
    // Ejecutar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectTabId);
    } else {
        injectTabId();
    }
    
    // También ejecutar en cada cambio de página (para SPAs)
    window.addEventListener('load', injectTabId);
    
    // Mostrar indicador visual de pestaña (opcional)
    const tabId = getTabId();
    console.log('Tab ID:', tabId);
    
})();
