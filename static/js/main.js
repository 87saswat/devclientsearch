
// FOR PAGINATION IN paginator.html, projects.html and profiles.html
    // get search form and page links (we got the below values from projects.html)
    let searcForm = document.getElementById('searchForm')
    let pageLinks = document.getElementsByClassName('page-link ')

    // Ensure SEARCH FROM EXISTS.. LOOP THROUGH ALL THE ITEMS
    if (searcForm){
        for (let i=0; pageLinks.length>i; i++){
            pageLinks[i].addEventListener("click", function (e) {
                e.preventDefault()

                // GET  THE DATA ATRRIBUTE
                let page = this.dataset.page

                // ADD HIDDEN SEARCH INPUT TO FORM
                searcForm.innerHTML += `<input value =${page} name = "page" hidden />` 

                // SUBMIT THE FORM
                searcForm.submit()

                })
        }
    }
