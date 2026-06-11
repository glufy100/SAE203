// Autocomplete produit partage entre plusieurs pages de commande.
// Entree principale: la page courante et les elements DOM attendus.
// Sortie: aucun retour explicite, le script agit directement sur l'UI.

/**
 * Initialise l'autocomplete des produits.
 * Entree:
 * - aucun parametre, le script lit le DOM lui-meme.
 * Sortie:
 * - aucun retour; attache des ecouteurs d'evenements et met a jour l'interface.
 */
function initProductAutocomplete() {
    const searchInput = document.getElementById('produit_search');
    const selectInput = document.getElementById('produit_id');
    const quantiteInput = document.getElementById('quantite');
    const apiUrl = document.body.getAttribute('data-api-url') || '/drive/api/produits/search/';

    // Si la page n'a pas le formulaire cible, on quitte sans effet de bord.
    if (!searchInput || !selectInput) {
        console.log('Autocomplete: elements manquants, initialisation ignoree');
        return;
    }

    const state = {
        timeoutId: null,
        suggestionsBox: null,
        formGroup: searchInput.parentElement,
    };

    /**
     * Cree la boite de suggestions.
     * Entree:
     * - formGroup: element DOM parent qui recevra la boite.
     * Sortie:
     * - HTMLElement de la boite de suggestions.
     */
    function createSuggestionsBox(formGroup) {
        const box = document.createElement('div');
        box.className = 'autocomplete-suggestions';
        box.style.display = 'none';
        formGroup.appendChild(box);
        return box;
    }

    /**
     * Masque la liste de suggestions.
     * Entree:
     * - box: element DOM de la liste.
     * Sortie:
     * - aucune.
     */
    function hideSuggestions(box) {
        if (box) {
            box.style.display = 'none';
        }
    }

    /**
     * Affiche un message dans la zone de suggestions.
     * Entree:
     * - box: element DOM cible.
     * - html: contenu HTML a afficher.
     * Sortie:
     * - aucune.
     */
    function setSuggestionsContent(box, html) {
        if (!box) {
            return;
        }
        box.innerHTML = html;
        box.style.display = 'block';
    }

    /**
     * Ajoute ou selectionne un produit dans le select.
     * Entree:
     * - produit: objet JSON renvoye par l'API, avec id, nom, prix, categorie, marque.
     * Sortie:
     * - aucune; met a jour le select, le champ de recherche et le focus.
     */
    function selectProduct(produit) {
        let option = selectInput.querySelector(`option[value="${produit.id}"]`);
        if (!option) {
            option = document.createElement('option');
            option.value = produit.id;
            option.textContent = produit.nom;
            selectInput.appendChild(option);
        }

        selectInput.value = produit.id;
        searchInput.value = produit.nom;
        hideSuggestions(state.suggestionsBox);

        // On enchaine directement sur la quantite pour fluidifier la saisie.
        if (quantiteInput) {
            quantiteInput.focus();
        }
    }

    /**
     * Transforme une liste de produits en carte de suggestions cliquables.
     * Entree:
     * - produits: tableau d'objets produits venant du backend.
     * Sortie:
     * - aucune; remplit la boite de suggestions.
     */
    function renderSuggestions(produits) {
        if (!state.suggestionsBox) {
            return;
        }

        state.suggestionsBox.innerHTML = '';

        if (!produits || produits.length === 0) {
            setSuggestionsContent(state.suggestionsBox, '<div class="autocomplete-item-empty">❌ Aucun produit trouvé</div>');
            return;
        }

        produits.forEach((produit) => {
            const item = document.createElement('div');
            item.className = 'autocomplete-item';
            item.innerHTML = `
                <strong>${produit.nom}</strong>
                <br><small>${produit.categorie} • ${produit.prix}€ • ${produit.marque}</small>
            `;

            item.addEventListener('click', () => {
                selectProduct(produit);
                console.log('Produit sélectionné:', produit.nom);
            });

            state.suggestionsBox.appendChild(item);
        });

        state.suggestionsBox.style.display = 'block';
    }

    /**
     * Interroge l'API de recherche de produits.
     * Entree:
     * - query: texte saisi par l'utilisateur.
     * Sortie:
     * - Promise<void>; met a jour l'UI au fur et a mesure de la resolution.
     */
    function fetchProducts(query) {
        const url = apiUrl + '?q=' + encodeURIComponent(query);
        console.log('Requete API:', url);

        return fetch(url)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                renderSuggestions(data.produits);
            })
            .catch((error) => {
                console.error('Erreur API:', error);
                setSuggestionsContent(
                    state.suggestionsBox,
                    `<div class="autocomplete-item-empty">⚠️ Erreur: ${error.message}</div>`
                );
            });
    }

    /**
     * Gere la saisie utilisateur dans le champ de recherche.
     * Entree:
     * - event: InputEvent provenant du champ texte.
     * Sortie:
     * - aucune; declenche ou annule la requete differée.
     */
    function handleSearchInput(event) {
        clearTimeout(state.timeoutId);
        const query = event.target.value.trim();

        if (query.length < 1) {
            hideSuggestions(state.suggestionsBox);
            return;
        }

        state.timeoutId = setTimeout(() => {
            fetchProducts(query);
        }, 300);
    }

    /**
     * Ferme les suggestions si le clic se produit en dehors du champ.
     * Entree:
     * - event: MouseEvent global du document.
     * Sortie:
     * - aucune; masque l'autocomplete si necessaire.
     */
    function handleDocumentClick(event) {
        if (event.target !== searchInput && state.suggestionsBox) {
            hideSuggestions(state.suggestionsBox);
        }
    }

    // La boite de suggestions est creee au premier focus pour ne pas polluer le DOM au chargement.
    searchInput.addEventListener('focus', function onSearchFocus() {
        if (!state.suggestionsBox) {
            state.suggestionsBox = createSuggestionsBox(state.formGroup);
            console.log('Autocomplete: boite de suggestions creee');
        }
    });

    // La saisie declenche une recherche differée.
    searchInput.addEventListener('input', handleSearchInput);

    // On ferme la liste lorsqu'on clique ailleurs dans la page.
    document.addEventListener('click', handleDocumentClick);
}

document.addEventListener('DOMContentLoaded', initProductAutocomplete);
