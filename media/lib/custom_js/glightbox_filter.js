var lightboxDescription = GLightbox({
        selector: 'glightbox'
    });


    function call(id) {
        // console.log("Working for " + id);
        active = Array.from(document.getElementsByClassName("filter-button"));
        active.map(function(item,x){
            item.classList.remove('active')
            
        })

        active.map(function(item,x){
            
            if(item.id===id){
                
                item.classList.add('active')
            }
            
        })


        const items = Array.from(document.getElementsByClassName("filter"));
        items.map(function (item, index) {
            
            if (id === "all") {
                item.classList.remove('d-none');
                item.classList.add('fadeIn', 'glightbox');
                setTimeout(clean, 500);
            } else {
                const check = items[index].classList.contains(id);
                console.log(check);

                if (check) {
                    item.classList.remove('d-none');
                    item.classList.add('fadeIn', 'glightbox');
                } else {
                    item.classList.add('d-none');
                    item.classList.remove('fadeIn', 'glightbox');
                }
            }
        })
        // console.log(items)
    }

    function clean() {
        const items = Array.from(document.getElementsByClassName("filter"));
        items.map(function (item, index) {
            item.classList.remove('fadeIn');
        })
    }