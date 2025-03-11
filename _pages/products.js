// Get references to modals and buttons
const addProductButton = document.getElementById("addProductButton");
const productModalOverlay = document.getElementById("productModalOverlay");
const closeProductModal = document.getElementById("closeProductModal");
const deleteModalOverlay = document.getElementById("deleteModalOverlay");
const closeDeleteModal = document.getElementById("closeDeleteModal");
const confirmDelete = document.getElementById("confirmDelete");
const cancelDelete = document.getElementById("cancelDelete");
const detailsModalOverlay = document.getElementById("detailsModalOverlay");
const closeDetailsModal = document.getElementById("closeDetailsModal");

// Variables to track current action and product
let currentProductRow = null;

// Add Product Button
addProductButton.addEventListener("click", () => {
  productModalOverlay.classList.add("active");
});

// Edit Product Buttons
document.querySelectorAll(".edit-product").forEach((button) => {
  button.addEventListener("click", (e) => {
    e.stopPropagation();
    currentProductRow = e.target.closest("tr");
    productModalOverlay.classList.add("active");
  });
});

// Delete Product Buttons
document.querySelectorAll(".delete-product").forEach((button) => {
  button.addEventListener("click", (e) => {
    e.stopPropagation();
    currentProductRow = e.target.closest("tr");
    deleteModalOverlay.classList.add("active");
  });
});

// Close Modals
closeProductModal.addEventListener("click", () => {
  productModalOverlay.classList.remove("active");
});

closeDeleteModal.addEventListener("click", () => {
  deleteModalOverlay.classList.remove("active");
});

cancelDelete.addEventListener("click", () => {
  deleteModalOverlay.classList.remove("active");
});

closeDetailsModal.addEventListener("click", () => {
  detailsModalOverlay.classList.remove("active");
});

// Confirm Delete
confirmDelete.addEventListener("click", () => {
  if (currentProductRow) {
    // Send a request to Django to delete the product
    // Django will handle the actual deletion and page reload
    deleteModalOverlay.classList.remove("active");
  }
});

// Show product details when a row is clicked
document.querySelectorAll(".product-row").forEach((row) => {
  row.addEventListener("click", (e) => {
    // Ignore clicks on buttons
    if (e.target.tagName === "BUTTON") return;

    // Show the details modal
    detailsModalOverlay.classList.add("active");
  });
});

// Close Product Details Modal when clicking outside
detailsModalOverlay.addEventListener("click", (e) => {
  if (e.target === detailsModalOverlay) {
    detailsModalOverlay.classList.remove("active");
  }
});