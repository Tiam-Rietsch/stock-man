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

    // Get product data from the row's data attribute
    const productData = JSON.parse(row.getAttribute("data-product"));

    // Populate the details modal with product data
    document.getElementById("detailsProductName").textContent = productData.name;
    document.getElementById("detailsBrand").textContent = productData.brand;
    document.getElementById("detailsCategory").textContent = productData.category;
    document.getElementById("detailsQuantity").textContent = productData.quantity;
    document.getElementById("detailsUnitPrice").textContent = `$${productData.unitPrice}`;
    document.getElementById("detailsProductImage").src = productData.image;

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

// Handle image upload
const uploadImageButton = document.getElementById("uploadImageButton");
const uploadImageInput = document.getElementById("uploadImage");
const productImage = document.getElementById("productImage");

uploadImageButton.addEventListener("click", (e) => {
  e.preventDefault(); // Prevent default button behavior
  uploadImageInput.click(); // Trigger the file input dialog
});

uploadImageInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      productImage.src = e.target.result; // Set the image source to the uploaded file
    };
    reader.readAsDataURL(file); // Read the file as a data URL
  }
});

// Handle form submission for adding/editing a product
const productForm = document.getElementById("productForm");

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
        // Handle success (e.g., reload the page or update the table)
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