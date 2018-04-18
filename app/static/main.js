
// update products in line via farmer.html
$(".update_col").on('click', function() {
	var rowIndex = $('#product_table tr').index($(this).closest('tr'))-1;
	var product = $(this).closest('tr').find('.product_col').text();
	var type = $(this).closest('tr').find('.type_col').text();
	var subtype = $(this).closest('tr').find('.subtype_col').text();
	var quantity = $(this).closest('tr').find('.quantity_col').text();
	var price = $(this).closest('tr').find('.price_col').text();
	var image = $(this).closest('tr').find('.image_col').text();
	var tr = $(this).closest("tr").remove().clone();

	// this if function makes sure the update occurs in the same table row rather than appending the update to the end of the table
	if (rowIndex == 0) {

		$('#product_table').prepend("<tr> <td class='product_col'><input value="+product+"></td> <td class='type_col'><input value="+type+"></td> <td class='subtype_col'><input value="+subtype+"></td> <td class='quantity_col'><input value="+quantity+"></td> <td class='price_col'><input value="+price+"></td> <td class='image_col'><input value="+image+"></td> <td class='submit_col'> <button class='submit_button'> Submit</button></td> </tr>");

} else {

	$('#product_table > tbody > tr').eq(rowIndex-1).after("<tr> <td class='product_col'><input value="+product+"></td> <td class='type_col'><input value="+type+"></td> <td class='subtype_col'><input value="+subtype+"></td> <td class='quantity_col'><input value="+quantity+"></td> <td class='price_col'><input value="+price+"></td> <td class='image_col'><input value="+image+"></td> <td class='submit_col'> <button class='submit_button'> Submit</button></td> </tr>");

}
	

});


$("#apply_filter_btn").on('click', function applyFilter() {
	var product = $('#product_filter').find('option:selected').text();
	var productType = $('#productType_filter').find('option:selected').text();
	var subType = $('#subType_filter').find('option:selected').text();
	
	filters = [product, productType,subType]
	console.log(filters);
	// console.log(subType);
	// var apply = {'product':product,'productType':productType,'subType':subType};

	$.post("apply-filter", {
 					product:product,
 					productType:productType,
 					subType:subType					

 			}).done(function (reply) {
                $(document.body.parentNode).html(reply);
                
            }
        );


});

