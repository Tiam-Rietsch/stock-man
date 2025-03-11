// Get references to modals and buttons
const addProductButton = document.getElementById("addProductButton");
const productModalOverlay = document.getElementById("productModalOverlay");
const closeProductModal = document.getElementById("closeProductModal");
const deleteModalOverlay = document.getElementById("deleteModalOverlay");
const closeDeleteModal = document.getElementById("closeDeleteModal");
const confirmDelete = document.getElementById("confirmDelete");
const cancelDelete = document.getElementById("cancelDelete");
const uploadImageButton = document.getElementById("uploadImageButton");
const uploadImageInput = document.getElementById("uploadImage");
const productImage = document.getElementById("productImage");
const productForm = document.getElementById("productForm");

// Variables to track current product card
let currentProductCard = null;

// Add Product Button
addProductButton.addEventListener("click", () => {
  // Reset the form for adding a new product
  productForm.reset();
  productImage.src = "placeholder.jpg";
  document.getElementById("modalTitle").textContent = "Add Product";
  productModalOverlay.classList.add("active");
});

// Edit Product Buttons
document.querySelectorAll(".edit-product").forEach((button) => {
  button.addEventListener("click", (e) => {
    e.stopPropagation();
    currentProductCard = e.target.closest(".product-card");

    // Get product data from the card's data attribute
    const productData = JSON.parse(currentProductCard.getAttribute("data-product"));

    // Populate the form with product data
    document.getElementById("productName").value = productData.name;
    document.getElementById("brand").value = productData.brand;
    document.getElementById("category").value = productData.category;
    document.getElementById("sid").value = productData.sid;
    document.getElementById("description").value = productData.description;
    document.getElementById("unitPrice").value = productData.unitPrice;
    productImage.src = productData.image;

    // Change the modal title
    document.getElementById("modalTitle").textContent = "Edit Product";

    // Open the product modal
    productModalOverlay.classList.add("active");
  });
});

// Delete Product Buttons
document.querySelectorAll(".delete-product").forEach((button) => {
  button.addEventListener("click", (e) => {
    e.stopPropagation();
    currentProductCard = e.target.closest(".product-card");
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

// Confirm Delete
confirmDelete.addEventListener("click", () => {
  if (currentProductCard) {
    // Remove the product card from the DOM
    currentProductCard.remove();
    deleteModalOverlay.classList.remove("active");
  }
});

// Handle image upload
uploadImageButton.addEventListener("click", (e) => {
  e.preventDefault();
  uploadImageInput.click();
});

uploadImageInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      productImage.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
});

// Handle form submission for adding/editing a product
productForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const formData = new FormData(productForm);

  // Append the uploaded image file to the form data
  if (uploadImageInput.files[0]) {
    formData.append("image", uploadImageInput.files[0]);
  }

  fetch("/your-django-endpoint/", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Handle success (e.g., reload the page or update the grid)
        window.location.reload();
      } else {
        // Handle error
        alert("There was an error submitting the form.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});