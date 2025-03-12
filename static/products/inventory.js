// Get references to modals and buttons
const addModalOverlay = document.getElementById("addModalOverlay");
const closeAddModal = document.getElementById("closeAddModal");
const editModalOverlay = document.getElementById("editModalOverlay");
const closeEditModal = document.getElementById("closeEditModal");
const searchInput = document.getElementById("searchInput");
const searchButton = document.getElementById("searchButton");

// Variables to track current product row
let currentProductRow = null;

// Add Quantity Button
document.querySelectorAll(".add-quantity").forEach((button) => {
  button.addEventListener("click", (e) => {
    e.stopPropagation();
    currentProductRow = e.target.closest("tr");

    // Get product data from the row's data attribute
    const productData = JSON.parse(currentProductRow.getAttribute("data-product"));
    
    // set the form action for the add form
    const stockAddUrl = button.getAttribute('stock-add-url')
    document.getElementById('addQuantityForm').setAttribute('action', stockAddUrl)

    // Populate the add modal with product data
    document.getElementById("addProductImage").src = productData.image;
    document.getElementById("addProductName").value = productData.name;
    document.getElementById("addBrand").value = productData.brand;
    document.getElementById("addCategory").value = productData.category;

    // Open the add modal
    addModalOverlay.classList.add("active");
  });
});

// Edit Quantity Button
document.querySelectorAll(".edit-quantity").forEach((button) => {
  button.addEventListener("click", (e) => {
    e.stopPropagation();
    currentProductRow = e.target.closest("tr");

    // Get product data from the row's data attribute
    const productData = JSON.parse(currentProductRow.getAttribute("data-product"));

    // set the form action for the edit form
    const stockEditUrl = button.getAttribute('stock-edit-url')
    document.getElementById('editQuantityForm').setAttribute('action', stockEditUrl)

    // Populate the edit modal with product data
    document.getElementById("editProductImage").src = productData.image;
    document.getElementById("editProductName").value = productData.name;
    document.getElementById("editBrand").value = productData.brand;
    document.getElementById("editCategory").value = productData.category;
    document.getElementById("editQuantity").value = productData.quantity;

    // Open the edit modal
    editModalOverlay.classList.add("active");
  });
});

// Close Modals
closeAddModal.addEventListener("click", () => {
  addModalOverlay.classList.remove("active");
});

closeEditModal.addEventListener("click", () => {
  editModalOverlay.classList.remove("active");
});


// Search functionality
searchButton.addEventListener("click", () => {
  const searchTerm = searchInput.value.toLowerCase();
  const rows = document.querySelectorAll(".product-row");

  rows.forEach((row) => {
    const productName = row.querySelector("td:nth-child(1)").textContent.toLowerCase();
    if (productName.includes(searchTerm)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
});