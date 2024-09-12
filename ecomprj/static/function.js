// Adding review : 
// console.log("From function.js");


const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"];

$("#commentForm").submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDate() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url : $(this).attr("action"),

        dataType : "json",

        success : function(res){
            console.log("comment saved to DB");

            if(res.bool == true ){
                $("#review-res").html("Review added Successfully.")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                let _html = '<div class="review-item"  style="display: flex; margin-bottom: 10px;margin-right:20px; padding: 1rem; border: 1px solid #ddd; border-radius: 10px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); transition: transform 0.3s ease, box-shadow 0.3s ease;">'
                    _html += '<img src="https://static.vecteezy.com/system/resources/thumbnails/020/765/399/small/default-profile-account-unknown-icon-black-silhouette-free-vector.jpg" alt="Reviewer Image" style="width: 80px; height: 80px; border-radius: 50%; margin-right: 1rem;">'
                    _html += '<div>'
                    _html += '<h4 style="margin: 0; font-size: 1.2rem;">'+ res.context.user +'</h4>'
                    _html += '<p style="margin: 0.5rem 0; font-size: 0.9rem; color: #666;">'+ time +'</p>'
                    _html += '<p style="font-size: 1rem;">'+ res.context.review +'</p>'
                    // _html += '<div class="review-rating" style="color: #ffc107;">'
                    for (let i = 1; i <= res.context.rating; i++ ) {
                        _html += '<i class="fas fa-star text-warning"></i>'
                    }
                    _html += '</div>'
                    _html += '</div>'
                    _html += '</div>'

                    
                    $(".reviews-section").prepend(_html);

            }
        }
    })
})


//  Add to cart function
$(".add-to-cart-btn").on("click", function(){
    
    let this_val = $(this) 
    let index = this_val.attr("data-index")

    let quantity = $(".product-quantity-" + index).val()
    let product_title = $(".product-title-new-" + index).val()
    let product_id = $(".product-id-" + index).val()
    let product_price = $(".current-product-price-" + index).text().trim();
    product_price = parseFloat(product_price.replace(/,/g, ''));
    product_price = Math.round(product_price * 100) / 100;
    console.log('Product price is :', product_price);
    let product_pid = $(".product-pid-" + index).val()
    let product_image = $(".product-image-" + index).val()

    console.log("Quantity ", quantity);
    console.log("product_title ", product_title);
    console.log("product_id ", product_id);
    console.log("product_pid ", product_pid);
    console.log("product_price ", product_price);
    console.log("product_image ", product_image);
    console.log("index ", index);
    console.log("current product ", this_val);

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': product_id,
            'pid': product_pid,
            'image': product_image,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
        },
        dataType: 'json',
        beforeSend: function() {
            console.log("Adding Product To cart");
        },
        success: function(response){
            this_val.html("✓");
            console.log("Added Product To cart");

            $(".cart-items-count").text(response.totalcartitems)
        }
    })
})


// Delete from cart
$(".delete-product").on("click", function(){

    let this_val = $(this)
    let product_id = $(this).attr("data-product")

    console.log("Product id : ", product_id);

    $.ajax({
        url : "/delete-from-cart",
        data : {
            "id" : product_id,
        },
        dataType : "json",
        beforeSend : function(){
            this_val.hide()
        },
        success : function(response){
            console.log(response);
            this_val.show()
            $(".cart-items-count").text(response.totalcartitems)
            $("#cart-list").html(response.data)
        },
    })
})

// download Invoice

function downloadInvoice() {
    const element = document.body;
    const options = {
        margin: 0.5,
        filename: 'invoice.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };
    html2pdf().from(element).set(options).save();
}


// Adding to wishlist

$(".add-to-wishlist").on("click", function() {
    let product_id = $(this).attr('data-product-item');
    let this_val = $(this);

    console.log(product_id);

    $.ajax({
        url: "/add-to-wishlist",
        type: "GET",
        data: {
            "id": product_id
        },
        dataType: "json",
        beforeSend: function() {
            console.log("Adding to wishlist");
        },
        success: function(response) {
            this_val.html("✓");  
            console.log("Added To Wishlist1");
            if (response.bool === true) {
                console.log("Added To Wishlist2");
                $('.count-in-wishlist').text(response.wishlist_count);
            }
        },
    });
});

//  Remove from wishlist 
$(".delete-wishlist-product").on("click", function(){

    let this_val = $(this)
    let wishlist_id = $(this).attr("data-wishlist-product")

    console.log("Wishlist id : ", wishlist_id);

    $.ajax({
        url : "/remove-from-wishlist",
        type: "GET",
        data : {
            "id" : wishlist_id,
        },
        dataType : "json",
        beforeSend : function(){
            // this_val.hide()
            console.log("Deleting Product from wishlist")
        },
        success : function(response){
            console.log("Deleted Product")
            $('.count-in-wishlist').text(response.wishlist_count);
            $("#wishlist-list").html(response.data);
            
        }
    })
})