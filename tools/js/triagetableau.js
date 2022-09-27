/**
 * TABLE HTML       
 * @param {HTMLTableElement} tableau tableau de tri
 * @param {number} colonne de triage
 * @param {boolean} asc ordre de tri
 * 
 */   

   function TriageDuTableauParColonne(tableau, colonne, asc = true) {

        //  sens de modificetion
        const dirModifier = asc ? 1 : -1;
        // Initialisation du tablau
        const tBody = tableau.tBodies[0];

        // lignes
        const rows = Array.from(tBody.querySelectorAll('tr'));

        // triage des colonnes

        const ColonnesTriees = rows.sort( (a,b) => {
            const aColText = a.querySelector(`td:nth-child(${ colonne + 1 })`).textContent.trim();
            const bColText = b.querySelector(`td:nth-child(${ colonne + 1 })`).textContent.trim();
            
            return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
        
        });

        //  enlever les anciennes valeus

        while (tBody.firstChild) {
            tBody.removeChild(tBody.firstChild);
        }

        //  ajouter les valeurs triies

        tBody.append(...ColonnesTriees);

        tableau.querySelectorAll("th").forEach(th => th.classList.remove('th-sort-asc', 'th-sort-desc'));
        tableau.querySelector(`th:nth-child(${colonne + 1})`).classList.toggle('th-sort-asc', asc);
        tableau.querySelector(`th:nth-child(${colonne + 1})`).classList.toggle('th-sort-desc', !asc);

   }

   document.querySelectorAll('.table-sortable th').forEach(headerCell => {
    headerCell.addEventListener('click', () =>{
            const tableElement = headerCell.parentElement.parentElement.parentElement;
            const hederindex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
            const CurrentIsAscending = headerCell.classList.contains('th-sort-asc');

            TriageDuTableauParColonne(tableElement, hederindex, !CurrentIsAscending);

        });
   });
