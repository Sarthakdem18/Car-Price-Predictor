document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const predictButton = document.getElementById('predictButton');
    const resultContainer = document.getElementById('resultContainer');
    const predictedPrice = document.getElementById('predictedPrice');
    const errorContainer = document.getElementById('errorContainer');
    const errorMessage = document.getElementById('errorMessage');
    const loadingSpinner = document.getElementById('loadingSpinner');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading spinner
        loadingSpinner.classList.remove('hidden');
        resultContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        predictButton.disabled = true;
        
        // Collect form data
        const formData = {
            brand: document.getElementById('brand').value,
            model: document.getElementById('model').value,
            vehicle_age: Number(document.getElementById('vehicle_age').value),
            km_driven: Number(document.getElementById('km_driven').value),
            seller_type: document.getElementById('seller_type').value,
            fuel_type: document.getElementById('fuel_type').value,
            transmission_type: document.getElementById('transmission_type').value,
            mileage: Number(document.getElementById('mileage').value),
            engine: Number(document.getElementById('engine').value),
            max_power: Number(document.getElementById('max_power').value),
            seats: Number(document.getElementById('seats').value)
        };
        
        try {
            // Make API call to your backend
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            if (!response.ok) {
                throw new Error('Failed to get prediction');
            }
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Display the prediction
            predictedPrice.textContent = '₹ ' + data.predicted_price.toLocaleString();
            resultContainer.classList.remove('hidden');
            
        } catch (error) {
            console.error('Error:', error);
            errorMessage.textContent = error.message || 'Failed to predict price. Please try again.';
            errorContainer.classList.remove('hidden');
        } finally {
            // Hide loading spinner
            loadingSpinner.classList.add('hidden');
            predictButton.disabled = false;
        }
    });
});