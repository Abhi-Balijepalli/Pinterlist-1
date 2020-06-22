

window.addEventListener('load', function(){
    var add_item = document.getElementById("add-item");

      
    var insert_item = add_item.addEventListener("keyup", function(event) {
        if (event.keyCode === 13) {
            
            // Cancel the default action, if needed
            event.preventDefault();
            // Trigger the button element with a click
            var item_text = add_item.value;
            addItem(item_text);
            
            this.value = '';
        }
    });

    // change class for checked items
   
    var toggle_checked_item = document.getElementById("item_list").addEventListener("click", function(e){
        console.log("item clicked")
        if (e.target && e.target.matches("li.return-recipe-item")) {
            e.target.classList.toggle("is_checked");
        }
    });

    //take away text on focus
    var item_text_focus = add_item.addEventListener('focus', function(){
        
        if (this.value != ''){
            this.value = '';
        }
    });
    
    // add helper text on blur
    var item_text_blur = add_item.addEventListener('blur', function(){
        
        if (this.value == ''){
            this.value = '+ Item';
        }
    });
    
    function addItem(item_text){
        //var currentURL = ;// need current URL somehow
        /*
        var request = XMLHttpRequest();
        var requestURL = "/pinToList/addIngredient";
        
        request.open('POST', requestURL);
        var requestBody = JSON.stringify({inputURL:currentURL,
        ingredient:item_text});
        
        request.setRequestHeader(
        'Content-Type', 'application/json');
        
        request.addEventListener('load', function(event){
        if(event.target.status === 200){
        
        
        
        //your code here
        
        }
        else{
        alert("error");
        
        }
        }
        request.send(requestBody);
        */
        var item_btn = document.getElementById("add-Item");
    
        
    
        var itemDiv = document.createElement('li');
        itemDiv.classList.add("return-recipe-item");
        itemDiv.textContent = item_text;
    
        //insert into page
        var list_container = document.getElementsByClassName("return-recipe-list")[0];
        list_container.prepend(itemDiv);
    }
    

});


