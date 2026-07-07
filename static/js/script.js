// Cold-Chain Expiry Accelerator - JavaScript Functions

// Confirmation for delete actions
function confirmDelete(itemName) {
    return confirm(`Are you sure you want to delete ${itemName}? This action cannot be undone.`);
}

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.classList.add('was-validated');
        return form.checkValidity();
    }
    return true;
}

// Temperature input validation
function validateTemperature(input) {
    const temp = parseFloat(input.value);
    if (isNaN(temp) || temp < -50 || temp > 50) {
        input.setCustomValidity('Temperature must be between -50°C and 50°C');
        return false;
    }
    input.setCustomValidity('');
    return true;
}

// Quantity validation
function validateQuantity(input) {
    const quantity = parseInt(input.value);
    if (isNaN(quantity) || quantity < 0) {
        input.setCustomValidity('Quantity must be a non-negative number');
        return false;
    }
    input.setCustomValidity('');
    return true;
}

// Date validation
function validateManufacturingDate(input) {
    const selectedDate = new Date(input.value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (selectedDate > today) {
        input.setCustomValidity('Manufacturing date cannot be in the future');
        return false;
    }
    input.setCustomValidity('');
    return true;
}

// Temperature comparison validation
function validateTemperatureComparison() {
    const idealTemp = document.getElementById('ideal_temperature');
    const maxTemp = document.getElementById('maximum_temperature');
    
    if (idealTemp && maxTemp) {
        const ideal = parseFloat(idealTemp.value);
        const max = parseFloat(maxTemp.value);
        
        if (!isNaN(ideal) && !isNaN(max) && max < ideal) {
            maxTemp.setCustomValidity('Maximum temperature cannot be less than ideal temperature');
            return false;
        }
        maxTemp.setCustomValidity('');
    }
    return true;
}

// Format number to 2 decimal places
function formatDecimal(number) {
    return parseFloat(number).toFixed(2);
}

// Status color helper
function getStatusColor(status) {
    const colors = {
        'Safe': 'success',
        'Warning': 'warning',
        'Critical': 'danger',
        'Expired': 'secondary'
    };
    return colors[status] || 'secondary';
}

// Calculate days until expiry
function calculateDaysUntil(expiryDate) {
    const today = new Date();
    const expiry = new Date(expiryDate);
    const diffTime = expiry - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
}

// Export table to CSV (client-side helper)
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(function(row) {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        cols.forEach(function(col) {
            csvRow.push('"' + col.innerText.replace(/"/g, '""') + '"');
        });
        csv.push(csvRow.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Search filter helper
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    input.addEventListener('keyup', function() {
        const filter = input.value.toUpperCase();
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const cells = row.getElementsByTagName('td');
            let found = false;
            
            for (let j = 0; j < cells.length; j++) {
                const cell = cells[j];
                if (cell) {
                    const textValue = cell.textContent || cell.innerText;
                    if (textValue.toUpperCase().indexOf(filter) > -1) {
                        found = true;
                        break;
                    }
                }
            }
            
            row.style.display = found ? '' : 'none';
        }
    });
}
