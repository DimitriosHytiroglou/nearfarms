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

// Javascript for the file upload button on product.html
var file = document.getElementById("file");
file.onchange = function(){
    if(file.files.length > 0)
    {

      document.getElementById('filename').innerHTML = 					file.files[0].name;

    }
};
