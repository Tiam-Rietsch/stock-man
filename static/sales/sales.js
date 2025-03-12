// Get references to form elements
const productSelect = document.getElementById("product");
const brandInput = document.getElementById("brand");
const categoryInput = document.getElementById("category");
const productImage = document.getElementById("productImage");
const unitPriceInput = document.getElementById("unitPrice");
const quantityInput = document.getElementById("quantity");
const totalPriceInput = document.getElementById("totalPrice");

const saleRows = document.querySelectorAll(".sale-row");
saleRows.forEach((row) => {
  row.addEventListener("click", () => {
    const sale = JSON.parse(row.getAttribute("data-sale"));
    populateForm(sale);
  });
});

// Function to populate form with sale data
// function populateForm(sale) {
//   productSelect.value = sale.product;
//   brandInput.value = sale.brand.toLowerCase();
//   categoryInput.value = sale.category;
//   productImage.src = sale.image;
//   unitPriceInput.value = sale.unitPrice;
//   quantityInput.value = sale.quantity;
//   totalPriceInput.value = sale.totalPrice;
// }

// Calculate total price dynamically
quantityInput.addEventListener("input", calculateTotalPrice);

function calculateTotalPrice() {
  const quantity = parseFloat(quantityInput.value) || 0;
  const unitPrice = parseFloat(unitPriceInput.value) || 0;
  totalPriceInput.value = (quantity * unitPrice).toFixed(2);
}

// listen to product selection
productSelect.addEventListener('change', (event) => {
  const selectedOption = productSelect.selectedOptions[0];
  const productData = JSON.parse(selectedOption.getAttribute('product-data'));
  brandInput.value = productData.brand;
  categoryInput.value = productData.category;
  productImage.src = productData.image;
  unitPriceInput.value = productData.unit_price;
  totalPriceInput.value = ""
  quantityInput.value = ""
  quantityInput.setAttribute('max', productData.quantity)
})