function placeOrder() {
    const fuelType = document.getElementById('plant-type').value;
    const quantity = document.getElementById('quantity').value;
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const payment = document.getElementById('payment').value;

    const orderDetails = {
        plantType,
        quantity,
        name,
        address,
        payment
    };

    fetch('/place_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderDetails)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error placing order:', error);
    });
    
}