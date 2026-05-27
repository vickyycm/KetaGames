/* ============================================
   KetaGames - Script Principal
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    console.log('KetaGames cargado correctamente');
    
    // Smooth scroll para navegación por anclas
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Solo prevenir default si es una ancla válida
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                
                const target = document.querySelector(href);
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

