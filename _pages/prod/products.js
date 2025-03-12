// Get references to modals and buttons
const addProductButton = document.getElementById("addProductButton");
const addModalOverlay = document.getElementById("addModalOverlay");
const closeAddModal = document.getElementById("closeAddModal");
const editModalOverlay = document.getElementById("editModalOverlay");
const closeEditModal = document.getElementById("closeEditModal");
const deleteModalOverlay = document.getElementById("deleteModalOverlay");
const closeDeleteModal = document.getElementById("closeDeleteModal");
const confirmDelete = document.getElementById("confirmDelete");
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

    // Populate the edit form with product data
    document.getElementById("editProductName").value = productData.name;
    document.getElementById("editBrand").value = productData.brand;
    document.getElementById("editCategory").value = productData.category;
    document.getElementById("editSid").value = productData.sid;
    document.getElementById("editDescription").value = productData.description;
    document.getElementById("editUnitPrice").value = productData.unitPrice;
    document.getElementById("editProductImage").src = productData.image;

    // Open the edit modal
    editModalOverlay.classList.add("active");
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

// Confirm Delete
confirmDelete.addEventListener("click", () => {
  if (currentProductCard) {
    // Remove the product card from the DOM
    currentProductCard.remove();
    deleteModalOverlay.classList.remove("active");
  }
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

// Handle form submission for adding a product
document.getElementById("addProductForm").addEventListener("submit", (e) => {
  e.preventDefault();

  const formData = new FormData(document.getElementById("addProductForm"));

  // Append the uploaded image file to the form data
  if (document.getElementById("addUploadImage").files[0]) {
    formData.append("image", document.getElementById("addUploadImage").files[0]);
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

// Handle form submission for editing a product
document.getElementById("editProductForm").addEventListener("submit", (e) => {
  e.preventDefault();

  const formData = new FormData(document.getElementById("editProductForm"));

  // Append the uploaded image file to the form data
  if (document.getElementById("editUploadImage").files[0]) {
    formData.append("image", document.getElementById("editUploadImage").files[0]);
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