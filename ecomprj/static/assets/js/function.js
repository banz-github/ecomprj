console.log("working fine");

const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
  "July", "Aug", "Sept", "Oct", "Nov", "Dec"
];

$("#commentForm").submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(), 

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(res){
            console.log("Comment Saved");

            if(res.bool == true){
                $("#review-res").html("Review added successfully")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="user justify-content-between d-flex">'
                    _html += '<div class="thumb text-center">'
                    _html += '<img src="https://i.pinimg.com/564x/65/25/a0/6525a08f1df98a2e3a545fe2ace4be47.jpg" alt="" />'
                    _html += '<a href="#" class="font-heading text-brand">'+ res.context.user +'</a>'
                    _html += '</div>'

                    _html += '<div class="desc">'
                    _html += '<div class="d-flex justify-content-between mb-10">'
                    _html += '<div class="d-flex align-items-center">'
                    _html += '<span class="font-xs text-muted">' + time + '</span>'
                    _html += '</div>'

                    for(var i=1; i<=res.context.rating; i++ ){
                        _html += '<i class="fas fa-star text-warning"></i>';
                    }


                    _html += '</div>'
                    _html += '<p class="mb-10">'+ res.context.review +'</p>'

                    _html += '</div>'
                    _html += '</div>'
                    _html += ' </div>'
                    $(".comment-list").prepend(_html)
                    
                }
                
                


        }
        })
})

$(document).ready(function (){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        console.log("A checkbox have been clicked");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter") // vendor, category

            // console.log("Filter value is:", filter_value);
            // console.log("Filter key is:", filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value
            })  
        })
        console.log("Filter Object is: ", filter_object);
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("Trying to filter product...");
            },
            success: function(response){
                console.log(response.length);
                console.log("Data filtred successfully...");
                $(".totall-product").hide()
                $("#filtered-product").html(response.data)
            }
        })
    })

    $("#max_price").on("blur", function(){
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        // console.log("Current Price is:", current_price);
        // console.log("Max Price is:", max_price);
        // console.log("Min Price is:", min_price);

        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            // console.log("Price Error Occured");

            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            
            // console.log("Max Price is:", min_Price);
            // console.log("Min Price is:", max_Price);

            alert("Price must between $" +min_price + ' and $' +max_price)
            $(this).val(min_price)
            $('#range').val(min_price)

            $(this).focus()

            return false
            
        }

    })
    
    // Add to cart functionality
    $(".add-to-cart-btn").on("click", function(){
    
        let this_val = $(this)
        let index = this_val.attr("data-index")
    
        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()
    
        let product_id = $(".product-id-" + index).val()
        let product_price = $(".current-product-price-" + index).text()
    
        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()
    
    
        console.log("Quantity:", quantity);
        console.log("Title:", product_title);
        console.log("Price:", product_price);
        console.log("ID:", product_id);
        console.log("PID:", product_pid);
        console.log("Image:", product_image);
        console.log("Index:", index);
        console.log("Currrent Element:", this_val);
    
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
            beforeSend: function(){
                console.log("Adding Product to Cart...");
            },
            success: function(response){
                // this_val.html("✓")
                this_val.html("<i class='fas fa-check-circle'></i>")

                console.log("Added Product to Cart!");
                $(".cart-items-count").text(response.totalcartitems)
    
    
            }
        })
    })

    $("#clearCart").on("click", function() {
        $.ajax({
            url: "/clear-cart/",
            dataType: "json",
            success: function(response) {
                if (response.success) {
                    // Cart cleared successfully, update UI
                    $(".cart-items-count").text(0); // Update the cart items count to 0
                    $("#cart-list").html(""); // Clear the cart items list
                    console.log("Cart cleared!");
    
                    // Display the success message
                    // Assuming you have an element with id "messages" to display messages
                    $("#messages").html('<div class="alert alert-warning">' + response.message + '</div>');
    
                    // Redirect to the home page after a short delay
                    setTimeout(function() {
                        window.location.href = "/";
                    }, 1); // 2000 milliseconds (2 seconds) delay, adjust as needed
                }
            }
        });
    });
    
    
    
    
    $(".delete-product").on("click", function(){
    
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
    
        console.log("PRoduct ID:",  product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Before Send");
                this_val.hide();
            },
            success: function(response){
                console.log("Success");
                this_val.show();
                $(".cart-items-count").text(response.totalcartitems);
                $("#cart-list").html(response.data);
            }
            
        })
    
    })



    
    $(".update-product").on("click", function(){
    
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-qty-"+product_id).val()
    
        console.log("PRoduct ID:",  product_id);
        console.log("PRoduct QTY:",  product_quantity);

        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "qty": product_quantity,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    
    })
    //Making Default
    $(document).on("click", ".make-default-address", function(){
        let id = $(this).attr("data-address-id")
        let this_val = $(this)
        console.log(" ID:", id);
        console.log("this_val :", this_val);

        $.ajax({
            url: "/make-default-address",
            data:{
                "id":id
            },
            dataType: "json",
            success: function(response){
                console.log("Default Address was changed");
                if ( response.boolean == true ){

                    $(".check").hide()
                    $(".action_btn").show()

                    $(".check"+id).show()
                    $(".button"+id).hide()
                    

                }
            }
        })

    })

    // try to geolocate

    // $(document).ready(function () {
    //     const addressTextarea = $("#address");
    //     const mobileInput = $("#mobile");
    //     const fetchLocationButton = $("#fetchLocation");
    
    //     fetchLocationButton.on("click", function () {
    //         if ("geolocation" in navigator) {
    //             navigator.geolocation.getCurrentPosition(function (position) {
    //                 const latitude = position.coords.latitude;
    //                 const longitude = position.coords.longitude;
        
    //                 // Format the location data
    //                 const locationData = `Latitude: ${latitude}, Longitude: ${longitude}`;
        
    //                 // Append the location data to the "location-data" container
    //                 $(".location-data").append(locationData);
        
    //                 // Optionally, you can clear the mobile input field
    //                 mobileInput.val("");
    //             }, function (error) {
    //                 console.error("Error getting location:", error);
    //                 alert("Unable to fetch location. Please enter your address manually.");
    //             });
    //         } else {
    //             alert("Geolocation is not supported in your browser. Please enter your address manually.");
    //         }
    //     });
        
    // });

    $(document).ready(function () {
        const addressTextarea = $("#address");
        const mobileInput = $("#mobile");
        const fetchLocationButton = $("#fetchLocation");
    
        fetchLocationButton.on("click", function () {
            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
    
                    // Use the Google Maps Geocoding API to convert coordinates to a human-readable address
                    const geocoder = new google.maps.Geocoder();
    
                    const location = new google.maps.LatLng(latitude, longitude);
                    geocoder.geocode({ 'location': location }, function (results, status) {
                        if (status === google.maps.GeocoderStatus.OK) {
                            if (results[0]) {
                                const formattedAddress = results[0].formatted_address;
                                addressTextarea.val(formattedAddress);
                            }
                        } else {
                            console.error("Geocoding failed with status: " + status);
                        }
                    });
    
                    // Optionally, you can clear the mobile input field
                    mobileInput.val("");
    
                }, function (error) {
                    console.error("Error getting location:", error);
                    alert("Unable to fetch location. Please enter your address manually.");
                });
            } else {
                alert("Geolocation is not supported in your browser. Please enter your address manually.");
            }
        });
    });
    
    
    //try to geolocate

    //adding to wishlist

    $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)

        console.log("Product ID is :", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id":product_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Adding to wishlist")
            },
            success: function(response){
                this_val.html("✓")
                if (response.bool === true){
                    console.log("Added to wishlist...");
                }
            }
        })

    })
    //remove from wishlist
    $(document).on("click", ".delete-wishlist-product", function(){
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("Wishlist ID is:", wishlist_id);

        $.ajax({
            url: "/remove-from-wishlist",
            data:{
                "id": wishlist_id
            },
            dataType: "json", 
            beforeSend: function(){
                console.log("deleting from wishlist...");
            },
            success:function(response){
                $("#wishlist-list").html(response.data)
            }
        })

    })

    $(document).on("submit", "#contact-form-ajax", function(e){
        e.preventDefault()
        console.log("submitted....");

        let full_name = $("#full_name").val()
        let email = $("#email").val()
        let phone = $("#phone").val()
        let subject = $("#subject").val()
        let message = $("#message").val()

        console.log("Name:", full_name);
        console.log("email:", email);
        console.log("phone:", phone);
        console.log("subject:", subject);
        console.log("message:", message);

        $.ajax({
            url: "/ajax-contact-form",
            data:{
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "subject": subject,
                "message": message,
            },
            dataType:"json",
            beforeSend:function(){
                console.log("Sending data to Server..");
            },
            success: function(res){
                console.log("Sent data to server");
                $(".contact_us_p").hide()
                $("#contact-form-ajax").hide()
                $("#message-response").html("Message sent successfully.")

            }
        })

    })

    //tryyyyyyyyyyy

    $(document).ready(function () {
        // Get references to the select and right-container elements
        const productTypeSelect = $('#product_type');
        const productTypeImage = $('#product-type-image'); // Updated this line

        // Add an event listener to the select element
        productTypeSelect.on('change', function () {
            const selectedOption = $(this).find('option:selected');

            // Check if a valid option is selected
            if (selectedOption.val()) {
                const productTypeId = selectedOption.val();

                // Make an AJAX request to retrieve the product type image
                $.ajax({
                    type: 'GET',
                    url: '/get_product_type_image/',  // Replace with the actual URL for retrieving images
                    data: { product_type_id: productTypeId },
                    success: function (response) {
                        // Update the product type image source
                        productTypeImage.attr('src', response.image_url); // Updated this line
                    },
                    error: function () {
                        console.log('Error loading product type image.');
                    }
                });
            }
        });
    });



    //tryyyyyyyyyy



})




// safety

// $(".add-to-cart-btn").on("click", function(){

//     let this_val = $(this)
//     let index = this_val.attr("data-index")

//     let quantity = $(".product-quantity-" + index).val()
//     let product_title = $(".product-title-" + index).val()

//     let product_id = $(".product-id-" + index).val()
//     let product_price = $(".current-product-price-"  + index).text()

//     let product_pid = $(".product-pid-"  + index).val()
//     let product_image = $(".product-image-" + index ).val()

//     console.log("Quantity:", quantity);
//     console.log("Id:", product_id);
//     console.log("Title:", product_title);
//     console.log("Price:", product_price);

//     console.log("product_pid:", product_pid);
//     console.log("product_image:", product_image);
//     console.log("index:", index);

//     console.log("This is:", this_val) ;

//     $.ajax({
//         url:'/add-to-cart',
//         data:{
//             'id':product_id,
//             'pid':product_pid,
//             'image':product_image,
//             'qty':quantity,
//             'title':product_title,
//             'price':product_price,
//         },
//         dataType:'json',
//         beforeSend:function(){
//             console.log("Added product to cart....");
//         },
//         success:function(response){
//             this_val.html("✓")
//             console.log("Added product to cart!");
//             $(".cart-items-count").text(response.totalcartitems)

//         }
//     })
// })

//     $(".delete-product").on("click", function(){
    
//         let product_id = $(this).attr("data-product")
//         let this_val = $(this)

//         console.log("PRoduct ID:",  product_id);

//         $.ajax({
//             url: "/delete-from-cart",
//             data: {
//                 "id": product_id
//             },
//             dataType: "json",
//             beforeSend: function(){
//                 this_val.hide()
//             },
//             success: function(response){
//                 this_val.show()
//                 $(".cart-items-count").text(response.totalcartitems)
//                 $("#cart-list").html(response.data)
//             }
//     })

    
    
        
// })















// $(".add-to-cart-btn").on("click", function(){
//     let quantity = $("#product-quantity").val()
//     let product_title = $(".product-title").val()
//     let product_id = $(".product-id").val()
//     let product_price = $("#current-product-price").text()
//     let this_val = $(this)

//     console.log("Quantity:", quantity);
//     console.log("Id:", product_id);
//     console.log("Title:", product_title)
//     console.log("Price:", product_price)
//     console.log("This is:", this_val) 

//     $.ajax({
//         url:'/add-to-cart',
//         data:{
//             'id':product_id,
//             'qty':quantity,
//             'title':product_title,
//             'price':product_price,
//         },
//         dataType:'json',
//         beforeSend:function(){
//             console.log("Added product to cart....");
//         },
//         success:function(response){
//             this_val.html("Added To Cart")
//             console.log("Added product to cart!");
//             $(".cart-items-count").text(response.totalcartitems)

//         }
//     })
// })







///////2nd safety



$(document).ready(function (){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        console.log("A checkbox have been clicked");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter") // vendor, category

            // console.log("Filter value is:", filter_value);
            // console.log("Filter key is:", filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value
            })  
        })
        console.log("Filter Object is: ", filter_object);
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("Trying to filter product...");
            },
            success: function(response){
                console.log(response.length);
                console.log("Data filtred successfully...");
                $(".totall-product").hide()
                $("#filtered-product").html(response.data)
            }
        })
    })

    $("#max_price").on("blur", function(){
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        //console.log("Current Price is:", current_price);
        // console.log("Max Price is:", max_price);
        // console.log("Min Price is:", min_price);

        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            // console.log("Price Error Occured");

            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            
            // console.log("Max Price is:", min_Price);
            // console.log("Min Price is:", max_Price);

            alert("Price must between ₱" +min_price + ' and ₱' +max_price)
            $(this).val(min_price)
            $('#range').val(min_price)

            $(this).focus()

            return false
            
        }

    })
})

//Add to cart Functionality


// $(".add-to-cart-btn").on("click", function(){
    
//     let this_val = $(this)
//     let index = this_val.attr("data-index")

//     let quantity = $(".product-quantity-" + index).val()
//     let product_title = $(".product-title-" + index).val()

//     let product_id = $(".product-id-" + index).val()
//     let product_price = $(".current-product-price-" + index).text()

//     let product_pid = $(".product-pid-" + index).val()
//     let product_image = $(".product-image-" + index).val()


//     console.log("Quantity:", quantity);
//     console.log("Title:", product_title);
//     console.log("Price:", product_price);
//     console.log("ID:", product_id);
//     console.log("PID:", product_pid);
//     console.log("Image:", product_image);
//     console.log("Index:", index);
//     console.log("Currrent Element:", this_val);

//     $.ajax({
//         url: '/add-to-cart',
//         data: {
//             'id': product_id,
//             'pid': product_pid,
//             'image': product_image,
//             'qty': quantity,
//             'title': product_title,
//             'price': product_price,
//         },
//         dataType: 'json',
//         beforeSend: function(){
//             console.log("Adding Product to Cart...");
//         },
//         success: function(response){
//             // this_val.html("✓")
//             this_val.html("<i class='fas fa-check-circle'></i>")

//             console.log("Added Product to Cart!");
//             $(".cart-items-count").text(response.totalcartitems)


//         }
//     })
// })


// $(".delete-product").on("click", function(){

//     let product_id = $(this).attr("data-product")
//     let this_val = $(this)

//     console.log("PRoduct ID:",  product_id);

//     $.ajax({
//         url: "/delete-from-cart",
//         data: {
//             "id": product_id
//         },
//         dataType: "json",
//         beforeSend: function(){
//             this_val.hide()
//         },
//         success: function(response){
//             this_val.show()
//             $(".cart-items-count").text(response.totalcartitems)
//             $("#cart-list").html(response.data)
//         }
//     })

// })




// $(".update-product").on("click", function(){

//     let product_id = $(this).attr("data-product")
//     let this_val = $(this)
//     // let product_quantity = $(".product-qty-"+product_id).val()

//     console.log("PRoduct ID:",  product_id);
//     // console.log("PRoduct QTY:",  product_quantity);

//     // $.ajax({
//     //     url: "/update-cart",
//     //     data: {
//     //         "id": product_id,
//     //         "qty": product_quantity,
//     //     },
//     //     dataType: "json",
//     //     beforeSend: function(){
//     //         this_val.hide()
//     //     },
//     //     success: function(response){
//     //         this_val.show()
//     //         $(".cart-items-count").text(response.totalcartitems)
//     //         $("#cart-list").html(response.data)
//     //     }
//     // })
    
// })