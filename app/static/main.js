
// update products in line via farmer.html
$(".update_col").on('click', function() {
	var rowIndex = $('#product_table tr').index($(this).closest('tr'))-1;
	var product = $(this).closest('tr').find('.product_col').text();
	var type = $(this).closest('tr').find('.type_col').text();
	var units = $(this).closest('tr').find('.units_col').text();
	var quantity = $(this).closest('tr').find('.quantity_col').text();
	var price = $(this).closest('tr').find('.price_col').text();
	var image = $(this).closest('tr').find('.image_col').text();
	var _id = $(this).closest('tr').find(":hidden").text();
	var tr = $(this).closest("tr").remove().clone();


	// this if function makes sure the update occurs in the same table row rather than appending the update to the end of the table
	if (rowIndex == 0) {

		$('#product_table').prepend("<tr> <td class='product_col'><input value="+product+"></td> <td class='type_col'><input value="+type+"></td> <td class='units_col'><input value="+units+"></td> <td class='quantity_col'><input value="+quantity+"></td> <td class='price_col'><input value="+price+"></td> <td class='image_col'><input value="+image+"></td> <td style='display:none' class='_id_col'>"+_id+"</td> <td class='submit_col'> <button type='button' class='submit_prod_button'> Submit</button></td> </tr>");

	} else {

	$('#product_table > tbody > tr').eq(rowIndex-1).after("<tr> <td class='product_col'><input value="+product+"></td> <td class='type_col'><input value="+type+"></td> <td class='units_col'><input value="+units+"></td> <td class='quantity_col'><input value="+quantity+"></td> <td class='price_col'><input value="+price+"></td> <td class='image_col'><input value="+image+"></td> <td style='display:none' class='_id_col'>"+_id+"</td> <td class='submit_col'> <button type='button' class='submit_prod_button'> Submit</button></td> </tr>");

	}
});

// UPDATE PRODUCT VALUES
$('body').on('click','.submit_prod_button','click', function() {


	var rowIndex = $('#product_table tr').index($(this).closest('tr'))-1;
	var product = $(this).closest('tr').find('.product_col').find('input').val();
	var productType = $(this).closest('tr').find('.type_col').find('input').val();
	var units = $(this).closest('tr').find('.units_col').find('input').val();
	var quantity = $(this).closest('tr').find('.quantity_col').find('input').val();
	var price = $(this).closest('tr').find('.price_col').find('input').val();
	var _id = $(this).closest('tr').find(":hidden").text();

	// var tr = $(this).closest("tr").remove().clone();

// THERE IS A MINOR ISSUE HERE BECAUSE THE AJAX IS SYNCHRONOUS, BUT IT ISNT!!

	$.post("product_update", {
 					product:product,
 					productType:productType,
 					units:units,
 					quantity:quantity,
 					price:price,
 					_id:_id					

 			}).done(function (reply) {
            window.location.reload(true);
            });
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
	

	$(this).closest('.card-content').find('.add_to_cart_button').css('display','none');
	$(this).closest('.card-content').find('.added_msg:hidden').css('display','block');

	$.post("add_to_shopping_cart", {
		product:product,
		productType:productType,
		units:units,
		price:price,
		marketID:marketID,
		product_id:product_id,
		ProducerID:ProducerID
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
			var quantity = $(this).closest('tr').find('.quantity_col').text();
			var price = $(this).closest('tr').find('.price_col').text();
			var marketID = $(this).closest('tr').find('.market_col').text();
			var _id = $(this).closest('tr').find("._id_col:hidden").text();
			var ProducerID = $(this).closest('tr').find(".ProducerID_col:hidden").text();
			var Product_id = $(this).closest('tr').find(".Product_id_col:hidden").text();

			var product_dict = {

				product: product,
				productType: productType,
				units: units,
				quantity: quantity,
				price: price,
				marketID: marketID,
				ProducerID:ProducerID,
				Product_id:Product_id,
				_id: _id
			}

			reserved_list.push(product_dict);
		}

    });

$.post("make_reservation", {
	reserved_list: JSON.stringify(reserved_list)
}).done(function (reply) {
    $(document.body).html(reply);               
              
    });
});




