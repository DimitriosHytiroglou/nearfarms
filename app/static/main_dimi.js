
$(".update_col").on('click', function() {
	var product = $(this).closest('tr').find('.product_col').text();
	var type = $(this).closest('tr').find('.type_col').text();
	var subtype = $(this).closest('tr').find('.subtype_col').text();
	var quantity = $(this).closest('tr').find('.quantity_col').text();
	var price = $(this).closest('tr').find('.price_col').text();
	var image = $(this).closest('tr').find('.image_col').text();
	var tr = $(this).closest("tr").remove().clone();
	
	$('#product_table').append("<tr> <td class='product_col'><input value="+product+"></td> <td class='type_col'><input value="+type+"></td> <td class='subtype_col'><input type="+subtype+"/></td> <td class='quantity_col'><input type="+quantity+"/></td> <td class='price_col'><input type="+price+"/></td> <td class='image_col'><input type="+image+"/></td> <button class='submit_button'> Submit</button></a></td> </tr>");

});


// // Event handler for clicking button of search box
// $(".update_col").on('click', function() {
    

// 	console.log('Click!');

// 	// console.log($(this).closest('tr'));
	

// 	var product = $(this).closest('tr').find('.product_col').text();
// 	var type = $(this).closest('tr').find('.type_col').text();
// 	var subtype = $(this).closest('tr').find('.subtype_col').text();
// 	var quantity = $(this).closest('tr').find('.quantity_col').text();
// 	var price = $(this).closest('tr').find('.price_col').text();
// 	var image = $(this).closest('tr').find('.image_col').text();
	

// 	$(this).parent().parent().append("<input>"+product+"</input>");

// 	// $(this).closest('td').append('<tr>Hello</tr>');
// 	// console.log($(this).closest('tr'));
// 	// $(this).closest().append("<p>Hello</p>");	

// 	$(this).parent("tr").remove();

	
	

// 	console.log(product,type,subtype);

// 	// $('.res').remove();

//  //    var user_input = $(this).parent().find('#search').val();
    
//  //    callAPI(user_input);

//  //    // Empty the input box
//  //    $(this).val('');

//  //    // set the counters to 0 to count from the beginning for the new results
//  //    printed = 0;
//  //   	i = 0;

// });

// $("#product_table").on('click', '.update', function() {
// 	var product = $(this).closest('tr').find('.product_col').text();
// 	var type = $(this).closest('tr').find('.type_col').text();
// 	var subtype = $(this).closest('tr').find('.subtype_col').text();
// 	var quantity = $(this).closest('tr').find('.quantity_col').text();
// 	var price = $(this).closest('tr').find('.price_col').text();
// 	var image = $(this).closest('tr').find('.image_col').text();
// 	var tr = $(this).closest("tr").remove().clone();
// 	$('#product_table').append("<tr> <td class='product_col'><input type="product"/></td> <td class='type_col'><input type="type"/></td> <td class='subtype_col'><input type="subtype"/></td> <td class='quantity_col'><input type="quantity"/></td> <td class='price_col'><input type="price"/></td> <td class='image_col'><input type="image"/></td> <button class='submit_button'> Submit</button></a></td> </tr>");

// });