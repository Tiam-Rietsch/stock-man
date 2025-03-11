// Get references to form elements
const productSelect = document.getElementById("product");
const brandSelect = document.getElementById("brand");
const categoryInput = document.getElementById("category");
const productImage = document.getElementById("productImage");
const unitPriceInput = document.getElementById("unitPrice");
const quantityInput = document.getElementById("quantity");
const totalPriceInput = document.getElementById("totalPrice");

// Add event listeners to sale rows
const saleRows = document.querySelectorAll(".sale-row");
saleRows.forEach((row) => {
  row.addEventListener("click", () => {
    const sale = JSON.parse(row.getAttribute("data-sale"));
    populateForm(sale);
  });
});

// Function to populate form with sale data
function populateForm(sale) {
  productSelect.value = sale.product.toLowerCase();
  brandSelect.value = sale.brand.toLowerCase();
  categoryInput.value = sale.category;
  productImage.src = sale.image;
  unitPriceInput.value = sale.unitPrice;
  quantityInput.value = sale.quantity;
  totalPriceInput.value = sale.totalPrice;
}

// Calculate total price dynamically
quantityInput.addEventListener("input", calculateTotalPrice);

function calculateTotalPrice() {
  const quantity = parseFloat(quantityInput.value) || 0;
  const unitPrice = parseFloat(unitPriceInput.value) || 0;
  totalPriceInput.value = (quantity * unitPrice).toFixed(2);
}