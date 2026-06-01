// ============================================
// AUTOCOMPLETE PRODUITS - Solution générique
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('produit_search');
    const selectInput = document.getElementById('produit_id');
    const quantiteInput = document.getElementById('quantite');
    const apiUrl = document.body.getAttribute('data-api-url') || '/drive/api/produits/search/';

    // Vérifications
    if (!searchInput || !selectInput) {
        console.log('❌ Autocomplete: Éléments manquants');
        return;
    }

    console.log('✅ Autocomplete activé');
    console.log('API URL:', apiUrl);

    let timeoutId;
    let suggestionsBox = null;
    const formGroup = searchInput.parentElement;

    // Créer la boîte de suggestions
    function createSuggestionsBox() {
        const box = document.createElement('div');
        box.className = 'autocomplete-suggestions';
        box.style.display = 'none';
        formGroup.appendChild(box);
        return box;
    }

    // Initialiser la boîte au focus
    searchInput.addEventListener('focus', function() {
        if (!suggestionsBox) {
            suggestionsBox = createSuggestionsBox();
            console.log('✅ Boîte suggestions créée');
        }
    });

    // Recherche au clavier
    searchInput.addEventListener('input', function() {
        clearTimeout(timeoutId);
        const query = this.value.trim();

        if (query.length < 1) {
            if (suggestionsBox) suggestionsBox.style.display = 'none';
            return;
        }

        console.log('🔍 Recherche:', query);

        timeoutId = setTimeout(() => {
            const url = apiUrl + '?q=' + encodeURIComponent(query);
            console.log('📡 Requête API:', url);

            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('📦 Résultats API:', data.produits.length);

                    if (suggestionsBox) {
                        suggestionsBox.innerHTML = '';

                        if (data.produits.length === 0) {
                            suggestionsBox.innerHTML = '<div class="autocomplete-item-empty">❌ Aucun produit trouvé</div>';
                        } else {
                            data.produits.forEach(produit => {
                                const item = document.createElement('div');
                                item.className = 'autocomplete-item';
                                item.innerHTML = `
                                    <strong>${produit.nom}</strong>
                                    <br><small>${produit.categorie} • ${produit.prix}€ • ${produit.marque}</small>
                                `;

                                item.addEventListener('click', () => {
                                    // Ajouter l'option si elle n'existe pas
                                    let option = selectInput.querySelector(`option[value="${produit.id}"]`);
                                    if (!option) {
                                        option = document.createElement('option');
                                        option.value = produit.id;
                                        option.textContent = produit.nom;
                                        selectInput.appendChild(option);
                                    }

                                    selectInput.value = produit.id;
                                    searchInput.value = produit.nom;
                                    suggestionsBox.style.display = 'none';

                                    if (quantiteInput) quantiteInput.focus();
                                    console.log('✅ Produit sélectionné:', produit.nom);
                                });

                                suggestionsBox.appendChild(item);
                            });
                        }

                        suggestionsBox.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('❌ Erreur API:', error);
                    if (suggestionsBox) {
                        suggestionsBox.innerHTML = `<div class="autocomplete-item-empty">⚠️ Erreur: ${error.message}</div>`;
                        suggestionsBox.style.display = 'block';
                    }
                });
        }, 300);
    });

    // Fermer au clic ailleurs
    document.addEventListener('click', function(e) {
        if (e.target !== searchInput && suggestionsBox) {
            suggestionsBox.style.display = 'none';
        }
    });
});