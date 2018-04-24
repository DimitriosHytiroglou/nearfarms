
// update products in line via farmer.html
$(".update_col").on('click', function() {
	var rowIndex = $('#product_table tr').index($(this).closest('tr'))-1;
	var market = $(this).closest('tr').find('.marketID_col').text();
	var product = $(this).closest('tr').find('.product_col').text();
	var type = $(this).closest('tr').find('.type_col').text();
	var units = $(this).closest('tr').find('.units_col').text();
	var quantity = $(this).closest('tr').find('.quantity_col').text();
	var price = $(this).closest('tr').find('.price_col').text();
	var _id = $(this).closest('tr').find(":hidden").text();
	
	console.log(_id);
	var tr = $(this).closest("tr").remove().clone();

	// this if function makes sure the update occurs in the same table row rather than appending the update to the end of the table
	if (rowIndex == 0) {

		$('#product_table').prepend("<tr> <td></td><td><select class='markets_filter'><option>"+market+"</option><option>Berkeley</option><option>Oakland</option><option>San Francisco</option></select></td> <td class='product_col'><input value=\""+product+"\"></td> <td class='type_col'><input value=\""+type+"\"></td> <td class='quantity_col'><input value="+quantity+"></td> <td class='price_col'><input value="+price+"></td> <td><select class='units_filter'><option>"+units+"</option><option>lbs</option><option>bunch</option><option>item</option></select></td><td style='display:none' class='_id_col'>"+_id+"</td> <td class='submit_col'> <button type='button' class='submit_prod_button'> Submit</button></td> </tr>");
                            

	} else {

	$('#product_table > tbody > tr').eq(rowIndex-1).after("<tr> <td></td><td><select class='markets_filter'><option>"+market+"</option><option>Berkeley</option><option>Oakland</option><option>San Francisco</option></select></td> <td class='product_col'><input value=\""+product+"\"></td> <td class='type_col'><input value=\""+type+"\"></td> <td class='quantity_col'><input value="+quantity+"></td> <td class='price_col'><input value="+price+"></td> <td><select class='units_filter'><option>"+units+"</option><option>lbs</option><option>bunch</option><option>item</option></select></td><td style='display:none' class='_id_col'>"+_id+"</td> <td class='submit_col'> <button type='button' class='submit_prod_button'> Submit</button></td> </tr>");

	}
});


// UPDATE PRODUCT VALUES
$('body').on('click','.submit_prod_button','click', function() {
	console.log("hello");

	var rowIndex = $('#product_table tr').index($(this).closest('tr'))-1;
	var market = $('.markets_filter').find('option:selected').text();
	var product = $(this).closest('tr').find('.product_col').find('input').val();
	var productType = $(this).closest('tr').find('.type_col').find('input').val();
	var quantity = $(this).closest('tr').find('.quantity_col').find('input').val();
	var price = $(this).closest('tr').find('.price_col').find('input').val();
	var units = $('.units_filter').find('option:selected').text();
	var _id = $(this).closest('tr').find("._id_col:hidden").text();

	console.log(_id);

	if (!Number.isInteger(Number(quantity)) || isNaN(Number(price))) {
		alert("Entry error: please enter price as a number and quantity as an integer.");
	}

// THERE IS A MINOR ISSUE HERE BECAUSE THE AJAX IS SYNCHRONOUS, BUT IT ISNT!!
	else {
	$.post("product_update", {
 					market:market,
 					product:product,
 					productType:productType,
 					units:units,
 					quantity:quantity,
 					price:price,
 					_id:_id					

 			}).done(function (reply) {
            window.location.reload(true);
            });
 		}
});

// DELETE PRODUCT FROM FARMER'S LIST
$(".remove_col").on('click', function() {
	var _id = $(this).closest('tr').find(":hidden").text();
// THERE IS A MINOR ISSUE HERE BECAUSE THE AJAX IS SYNCHRONOUS, BUT IT ISNT!!
	$.post("product_delete", {
 					_id:_id					
 			}).done(function (reply) {
            window.location.reload(true);
            });
});


// DELETE PRODUCT FROM SHOPPING CART
$(".remove_col_cart").on('click', function() {
	var _id = $(this).closest('tr').find("._id_col").text();
	console.log(_id);
// THERE IS A MINOR ISSUE HERE BECAUSE THE AJAX IS SYNCHRONOUS, BUT IT ISNT!!
	$.post("product_delete_cart", {
 					_id:_id					
 			}).done(function (reply) {
            window.location.reload(true);
            });
});









// Apply filters
$("#apply_filter_btn").on('click', function applyFilter() {
	var product = $('#product_filter').find('option:selected').text();
	var productType = $('#productType_filter').find('option:selected').text();
	var MarketID = $('#market_filter').find('option:selected').text();
	

	filters = [product, productType,MarketID]
	// console.log(subType);
	// var apply = {'product':product,'productType':productType,'subType':subType};

	$.post("apply-filter", {
 					product:product,
 					productType:productType,
 					MarketID:MarketID					

 			}).done(function (reply) {
                $(document.body).html(reply);
                
            });
});


// DIMITRIS
//  NOTE TO SELF, put the product id's in the id attribute instead of hidden HTML 

// Pull data for shopping cart from add to cart button
$('body').on('click','.add_to_cart_button','click', function() {

	var product = $(this).closest('.card-content').find('.product_detail').text();
	var productType = $(this).closest('.card-content').find('.productType_detail').text();
	var units = $(this).closest('.card-content').find('.units_detail').text();
	var price = $(this).closest('.card-content').find('.price_detail').text();
	var marketID = $(this).closest('.card-content').find('.marketID_detail').text();

	var product_id = $(this).closest('.card-content').find("._id_detail:hidden").text();
	var ProducerID = $(this).closest('.card-content').find(".ProducerID_detail:hidden").text();
	var quantity = $(this).closest('.card-content').find(".amount_detail").find ('.quantity_cart_filter').find('option:selected').text();

	$(this).closest('.card-content').find('.add_to_cart_button').css('display','none');
	$(this).closest('.card-content').find('.added_msg:hidden').css('display','block');

	$.post("add_to_shopping_cart", {
		product:product,
		productType:productType,
		units:units,
		price:price,
		marketID:marketID,
		product_id:product_id,
		ProducerID:ProducerID,
		quantity:quantity
	}).done(function (reply) {
                
                window.location.reload(true);
                
            
});
	});



// FUNCTION TO INCREMENT OR DECREMENT QUANTITY ON SHOPPING CART PAGE

$('.pos_increment_col').on('click',function() {
	var quantity = $(this).closest('tr').find('.quantity_col').text();
	var quantity_int = parseInt(quantity) +1
	$(this).closest('tr').find('.quantity_col').text(quantity_int);
});

$('.neg_increment_col').on('click',function() {
	var quantity = $(this).closest('tr').find('.quantity_col').text();
	var quantity_int = parseInt(quantity) - 1

	if (quantity_int >=0) {
		$(this).closest('tr').find('.quantity_col').text(quantity_int);
	}
	
});

// Gets value from dropdown on farmer's page
 $("#farmers_market").change(function () {
    var MarketID = this.value;

    $.post("apply-filter-farmer", {
		MarketID:MarketID
	}).done(function (reply) {
                $(document.body).html(reply);
                       
            });
    });


// SHOPPING CART PAGE CHANGE TOTAL PRICE BASED ON CHANGE QUANTITY
 $(".quantity_cart_filter").change(function () {
    var quantity = this.value;
    var price = $(this).closest('tr').find('.price_col').text();
    var totalPrice = '$'+String((quantity*price).toFixed(2));
    $(this).closest('tr').find('.totalPrice_col').text(totalPrice);

    });








// FUNCTION TO PULL AND PUSH DATA INTO RESERVATIONS PAGE
// Function to change value to true or false based on whether box is checked or not
 $(".checkbox").on("click", function () { 
      var checkbox = $(this).closest( ".checkbox" );
			checkbox.val( checkbox[0].checked ? "true" : "false" );
 });

// function to post reservation data
$(".reserve_button").on("click", function() {
	var reserved_list = []

	// function to pull data based on whether box is checked or not
	$('tbody').find('tr').each(function (i, el) {
		var checkbox = $(this).find(".checkbox")

		if (checkbox.val() == "true") {
			var product = $(this).closest('tr').find('.product_col').text();
			var productType = $(this).closest('tr').find('.type_col').text();
			var units = $(this).closest('tr').find('.units_col').text();
			var quantity = $(this).closest('tr').find(".quantity_cart_filter").find('option:selected').text();
			var price = $(this).closest('tr').find('.price_col').text();
			var totalPrice = $(this).closest('tr').find('.totalPrice_col').text();
			var marketID = $(this).closest('tr').find('.market_col').text();
			var _id = $(this).closest('tr').find("._id_col:hidden").text();
			var ProducerID = $(this).closest('tr').find(".ProducerID_col:hidden").text();
			var Product_id = $(this).closest('tr').find(".Product_id_col:hidden").text();

			// condition to check if quantity doesn't equal zero
			if (Number.parseInt(quantity) !=0) {
				var product_dict = {

					product: product,
					productType: productType,
					units: units,
					quantity: quantity,
					price: price,
					marketID: marketID,
					ProducerID:ProducerID,
					Product_id:Product_id,
					totalPrice:totalPrice,
					_id: _id
				}

				reserved_list.push(product_dict);
			}
		}

    });

$.post("make_reservation", {
	reserved_list: JSON.stringify(reserved_list)
}).done(function (reply) {
    $(document.body).html(reply);               
              
    });
});




