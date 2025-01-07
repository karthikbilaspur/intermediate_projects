// Image Upload Preview

function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
  
      reader.onload = function (e) {
        $('#image-preview').attr('src', e.target.result);
      };
  
      reader.readAsDataURL(input.files[0]);
    }
  }
  
  $("#image-upload").change(function () {
    readURL(this);
  });
  
  // Extracted Text Auto-Resize
  
  $(document).ready(function () {
    $('#extracted-text').on('input', function () {
      this.style.height = 'auto';
      this.style.height = (this.scrollHeight) + 'px';
    });
  });
  
  // Navigation Toggle
  
  function toggleNavigation() {
    var navigation = document.querySelector('nav');
    navigation.classList.toggle('active');
  }
  
  document.querySelector('.toggle-navigation').addEventListener('click', toggleNavigation);