// Get references to modals and buttons
const addProductButton = document.getElementById("addProductButton");
const addModalOverlay = document.getElementById("addModalOverlay");
const closeAddModal = document.getElementById("closeAddModal");
const editModalOverlay = document.getElementById("editModalOverlay");
const closeEditModal = document.getElementById("closeEditModal");
const deleteModalOverlay = document.getElementById("deleteModalOverlay");
const closeDeleteModal = document.getElementById("closeDeleteModal");
const cancelDelete = document.getElementById("cancelDelete");

// Variables to track current product card
let currentProductCard = null;

// Add Product Button
addProductButton.addEventListener("click", () => {
  // Reset the form for adding a new product
  document.getElementById("addProductForm").reset();
  document.getElementById("addProductImage").src = "placeholder.jpg";
  addModalOverlay.classList.add("active");
});

// Edit Product Buttons
document.querySelectorAll(".edit-product").forEach((button) => {
  button.addEventListener("click", (e) => {
    e.stopPropagation();
    currentProductCard = e.target.closest(".product-card");

    // Get product data from the card's data attribute
    const productData = JSON.parse(currentProductCard.getAttribute("data-product"));

    // get the url to which the post request should be sent and add it to the form
    const editUrl = button.getAttribute("edit-url");
    document.getElementById("editProductForm").setAttribute("action", editUrl)

    // Populate the edit form with product data
    document.getElementById("editProductName").value = productData.name;
    document.getElementById("editBrand").value = productData.brand;
    document.getElementById("editCategory").value = productData.category;
    document.getElementById("editSid").value = productData.sid;
    document.getElementById("editDescription").value = productData.description;
    document.getElementById("editUnitPrice").value = productData.unitPrice;
    document.getElementById("editProductImage").src = productData.image;
    document.getElementById("editMinStock").value = productData.min_stock;

    // Open the edit modal
    editModalOverlay.classList.add("active");
  });
});

// Delete Product Buttons
document.querySelectorAll(".delete-product").forEach((button) => {
  button.addEventListener("click", (e) => {
    e.stopPropagation();
    currentProductCard = e.target.closest(".product-card");

    const deleteUrl = button.getAttribute("delete-url")
    document.getElementById("deleteProductForm").setAttribute("action", deleteUrl)

    deleteModalOverlay.classList.add("active");
  });
});

// Close Modals
closeAddModal.addEventListener("click", () => {
  addModalOverlay.classList.remove("active");
});

closeEditModal.addEventListener("click", () => {
  editModalOverlay.classList.remove("active");
});

closeDeleteModal.addEventListener("click", () => {
  deleteModalOverlay.classList.remove("active");
});

cancelDelete.addEventListener("click", () => {
  deleteModalOverlay.classList.remove("active");
});

// Handle image upload for Add Modal
document.getElementById("addUploadImageButton").addEventListener("click", (e) => {
  e.preventDefault();
  document.getElementById("addUploadImage").click();
});

document.getElementById("addUploadImage").addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      document.getElementById("addProductImage").src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
});

// Handle image upload for Edit Modal
document.getElementById("editUploadImageButton").addEventListener("click", (e) => {
  e.preventDefault();
  document.getElementById("editUploadImage").click();
});

document.getElementById("editUploadImage").addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      document.getElementById("editProductImage").src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
});


