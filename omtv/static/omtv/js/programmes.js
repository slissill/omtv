function scrollToBottom(itemId) {
    // Récupérer l'élément qui a été déplié
    var targetElement = document.getElementById("programme-" + itemId);        
    // Vérifier si l'élément est visible
    if (targetElement) {
    // Utiliser setTimeout pour s'assurer que l'élément est visible après son déploiement
    setTimeout(function() {
        // Faire défiler la fenêtre jusqu'au bas de l'élément déplié
        targetElement.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }, 300); // ajustez la durée en millisecondes en fonction de la vitesse de déploiement de votre accordéon
    }
}

function getCollapsedDivs(isCollapsed) {
    var collapseElements = document.querySelectorAll("div[my_type='collapsable']");
    var divs = [];
    for (var i = 0; i < collapseElements.length; i++) {
        var element = collapseElements[i];
        var isElementCollapsed = element.classList.contains('collapse') && !element.classList.contains('show');                                
        if ((isCollapsed && isElementCollapsed) || (!isCollapsed && !isElementCollapsed)) {
            divs.push(element);
        }
    }            
    return divs;
}


function toggle_divs() {
    var divs_opened = getCollapsedDivs(false);
    var divs_closed = getCollapsedDivs(true);            
    var divs = divs_opened.length > 0 ? divs_opened : divs_closed;
    divs.forEach(function(element) {
        var bsCollapse = new bootstrap.Collapse(element, {toggle: true});
    })
}