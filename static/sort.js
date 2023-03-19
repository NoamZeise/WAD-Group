document.addEventListener('DOMContentLoaded', () => {

    const sortForm = document.getElementById('sort-form');
    const sortBy = document.getElementById('sort_by');
    const order = document.getElementById('sorting_order');
    const orderToggleButton = document.getElementById('order_toggle_button');

    if (sortForm && sortBy && order && orderToggleButton){
        orderToggleButton.innerHTML = order.value == 'ascending' ? '&#9650;' : '&#9660;';

        sortBy.addEventListener('change', () => {
            sortForm.submit();
        });
    
        orderToggleButton.addEventListener('click', () => {
            submitForm(order, orderToggleButton, sortForm);
        });
    }
})

function submitForm(order, orderToggleButton, sortForm){
    if (order.value == 'ascending'){
        order.value = 'descending';
        orderToggleButton.innerHTML = '&#9660;';
    }
    else {
        order.value = 'ascending';
        orderToggleButton.innerHTML = '&#9650;';
    }
    sortForm.submit();
}